import os
import pandas as pd
import re
from typing import Tuple
import openai
import asyncio
from tqdm import tqdm

def normalize_text(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)  # keep alphanumeric
    return s.strip()

def normalize_entities(s: str) -> set:
    """Split by commas/and and normalize names into a set."""
    s = re.sub(r"\band\b", ",", s, flags=re.IGNORECASE)
    parts = [normalize_text(x) for x in s.split(",")]
    return {p.strip() for p in parts if p.strip()}

def f1_score(prediction: str, ground_truth: str) -> float:
    """Compute token-level F1."""
    pred_tokens = normalize_text(prediction).split()
    gold_tokens = normalize_text(ground_truth).split()

    common = set(pred_tokens) & set(gold_tokens)
    num_same = sum(min(pred_tokens.count(w), gold_tokens.count(w)) for w in common)
    
    if len(pred_tokens) == 0 or len(gold_tokens) == 0:
        return float(pred_tokens == gold_tokens)
    if num_same == 0:
        return 0.0
    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)

def exact_match_score(prediction: str, ground_truth: str) -> float:
    """Check if normalized prediction exactly matches normalized ground truth."""
    return float(normalize_text(prediction) == normalize_text(ground_truth))
    
def set_match_score(prediction: str, ground_truth: str) -> float:
    pred_set = normalize_entities(prediction)
    gold_set = normalize_entities(ground_truth)

    em = float(pred_set == gold_set)
    
    if not pred_set or not gold_set:
        return em, float(pred_set == gold_set)
    
    common = pred_set & gold_set
    precision = len(common) / len(pred_set)
    recall = len(common) / len(gold_set)
    f1 = 2 * precision * recall / (precision + recall) if common else 0.0
    return em, f1

def qa_score_single(pred: str, gold: str, set_based=False) -> Tuple[float, float]:
    """Return (EM, F1) for a single QA pair."""
    if not set_based:
        return exact_match_score(pred, gold), f1_score(pred, gold)
    else:
        return set_match_score(pred, gold)

def bleu_score(prediction: str, ground_truth: str) -> float:
    """Compute BLEU score for single prediction and ground truth."""
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    pred_tokens = normalize_text(prediction).split()
    gold_tokens = normalize_text(ground_truth).split()
    smoothie = SmoothingFunction().method4
    return sentence_bleu([gold_tokens], pred_tokens, smoothing_function=smoothie)

def evaluate_dataset(path: str, gold_path: str, pred_col: str = "Answer") -> dict:
    """Evaluate a CSV or Parquet file with columns Question, Answer, Prediction."""
    if path.endswith(".csv"):
        df = pd.read_csv(path, delimiter=";")
        gold_df = pd.read_csv(gold_path, delimiter=";")
    elif path.endswith(".parquet"):
        df = pd.read_parquet(path)
        gold_df = pd.read_parquet(gold_path)
    else:
        raise ValueError("File must be .csv or .parquet")

    ems, f1s, bleus = [], [], []
    for (_, row) in df.iterrows():
        gold = gold_df.loc[gold_df["id"] == row["id"], "Answer"].values[0]
        print("Gold:", gold)
        pred = str(row[pred_col])
        em, f1 = qa_score_single(pred, gold)
        b_score = bleu_score(pred, gold)
        ems.append(em)
        f1s.append(f1)
        bleus.append(b_score)

    return {
        "EM": sum(ems) / len(ems),
        "F1": sum(f1s) / len(f1s),
        "BLEU": sum(bleus) / len(bleus),
    }

PROMPT_TEMPLATE = """
Besvar spørgsmålet med kun det direkte svar, uden forklaring om hvorfor.
Regelsæt:
- Svar kun på dansk.
- Hvis svaret er i højde, svar i meter (m).
- Hvis svaret er i vægt, svar i kilogram (kg).
- Hvis svaret er om en størrelse, svar i centimeter (cm). Fx Hvor stort er maleriet Mona Lisa? Svar: 77 cm x 53 cm.
- Hvis svaret er en person angiv den måde de typisk bliver angivet på i danske tekster.

\n\nSpørgsmål: {question}\nSvar:"""

async def get_prediction(client, model, identifier, question, expected, max_tokens=100, temperature=0.0):
    prompt = PROMPT_TEMPLATE.format(question=question)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    if response is None or response.choices is None or response.choices[0].message.content is None:
        print(f"Question {identifier}: Response is None")
        prediction = None
    else:
        print(response)
        prediction = response.choices[0].message.content.strip().replace("\n", " ")

    result = {
        "id": identifier,
        "question": question,
        "expected": expected,
        "prediction": prediction,
    }
    if expected is not None:
        result["correct"] = prediction.lower() == expected.lower()
    return result

async def call_api(input_file: str, output_file: str, model:str, base_url: str, api_key: str, max_tokens=100, temperature=0.0, batch_size=20, flush=False) -> str:
    client = openai.AsyncOpenAI(base_url=base_url, api_key=api_key)

    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file, delimiter=";")
    elif input_file.endswith(".parquet"):
        df = pd.read_parquet(input_file)
    
    tasks = []
    results = []
    print("Creating tasks...")
    for row in df.itertuples():
        print(f"Processing question: {row.Question}")
        expected = row.Answer if hasattr(row, 'Answer') else None
        tasks.append(
            get_prediction(client=client, model=model, identifier=row.id, question=row.Question, expected=expected, max_tokens=max_tokens, temperature=temperature)
        )
    print(f"Total questions to process: {len(df)}")

    if output_file is None:
        output_file = model.replace("/", "-") + "-predictions.csv"
        print(output_file)
    print(f"Writing predictions to {output_file}")

    if not output_file:
        output_file = model.replace("/", "-") + "-predictions.csv"
    
    with open(output_file, "w") as f:
        f.write("id;Answer\n")

        for i in tqdm(range(0, len(tasks), batch_size), desc="Processing batches"):
            batch = tasks[i:i+batch_size]
            batch_responses = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_responses)
    
            for i, response in enumerate(batch_responses):
                if response['prediction'] is None:
                    f.write(f"{response['id']};Error\n")
                else:
                    f.write(f"{response['id']};{response['prediction']}\n")

            if flush:  
                f.flush()

def run_eval(input_file: str, output_file: str, model:str, base_url: str, api_key: str, max_tokens=100, temperature=0.0):
    responses = asyncio.run(
        call_api(
            input_file=input_file,
            output_file=output_file,
            model=model,
            base_url=base_url,
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=temperature
        )
    )