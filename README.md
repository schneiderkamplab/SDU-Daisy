# SDUs Daisy: A Benchmark for Danish Culture 
<p align="center">
  <img src="docs/daisy_logo.png" alt="Description" width="250"/>
</p>


**SDU DAISY** is the first version of a dataset designed to **evaluate large language models’ understanding of Danish culture**, as defined by the official **Danish Culture Canon (Kulturkanon, 2006)**, defined by 746 closed question-answer pairs.  

The Canon highlights 108 works across literature, music, visual arts, architecture, design, film, and performing arts. These works form a curated benchmark of what is often considered Denmark’s cultural heritage. By using them as anchors, this dataset enables systematic investigation of how well LLMs can reason about, contextualize, and generate insights into Danish culture.  

---

## Why this dataset?  

- **Cultural Relevance Test** – The Canon provides a well-defined cultural benchmark for evaluation.  
- **Knowledge Probing** – Randomized prompts (Danish "*stikprøvekontrol*) test both relevant and less relevant associations with Canon works.
- **Human Validation** – Every generated question/response pair is annotated for validation and relevance, even though we both want to main- and non-mainstream knowledge. 

---

## Methodology  

1. **Sampling (*Stikprøvekontrol*)**  
   For each Canon title, random questions are generated — ranging from directly relevant inquiries (e.g., about historical context) to more peripheral or unexpected ones.  

2. **Response Collection**  
   LLMs provide answers to these questions, creating a structured dataset of outputs.  

3. **Human Evaluation**  
   - **Relevance** (on-topic vs. off-topic)  
   - **Accuracy** (correct vs. incorrect)  
   - **Cultural Insight** (does it capture nuance/meaning? - also including small or even niece facts)  

---

## Applications 

- Benchmarking **LLM performance on Danish culturally sub-domains**  
- Supporting **digital humanities research** on how AI engages with cultural canons  
- Encouraging critical reflection on the **boundaries of cultural knowledge** encoded in AI systems  

---

# SDU Daisy Evaluations 
<!-- <table style="width:100%; border-collapse:collapse;">
  <tr>
    <th style="text-align:left;">Model</th>
    <th style="text-align:center;">F1 Score</th>
    <th style="text-align:center;">Bleu</th>
    <th style="text-align:center;">Dataset version</th>
    <th style="text-align:center;">Prompt Template Version</th>
  </tr>
  <tr>
    <td>openai/gpt-oss-20b</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">1.0</td>
    <td style="text-align:center;">1.0</td>
  </tr>
  <tr>
    <td>openai/gpt-oss-120b</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">1.0</td>
    <td style="text-align:center;">1.0</td>
  </tr>
  <tr>
    <td>google/gemma-3-27b-it</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">-</td>
    <td style="text-align:center;">1.0</td>
    <td style="text-align:center;">1.0</td>
  </tr>
</table>
 -->
<style>
  .futuristic-table {
    width: 100%;
    border-collapse: collapse;
    font-family: system-ui, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 0 12px rgba(0,255,255,0.15);
  }
  .futuristic-table th {
    background: rgba(9,21,54,1.0); linear-gradient(135deg, #cf1846ff, #2421d1ff);
    color: white;
    text-align: center;
    padding: 12px;
    font-weight: 600;
    text-shadow: 0 0 6px rgba(255,255,255,0.4);
  }
  .futuristic-table td {
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .futuristic-table tr:nth-child(even) {
    background: rgba(255,255,255,0.03);
  }
  .futuristic-table tr:hover {
    background: rgba(0,255,255,0.08);
    transition: 0.2s;
  }
</style>

<table class="futuristic-table">
  <tr>
    <th>Model</th>
    <th>F1 Score</th>
    <th>Bleu</th>
    <th>Dataset version</th>
    <th>Prompt Template Version</th>
  </tr>
  <tr>
    <td style="text-align:left;">openai/gpt-oss-20b</td>
    <td>-</td>
    <td>-</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
  <tr>
    <td style="text-align:left;">openai/gpt-oss-120b</td>
    <td>-</td>
    <td>-</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
  <tr>
    <td style="text-align:left;">google/gemma-3-27b-it</td>
    <td>-</td>
    <td>-</td>
    <td>1.0</td>
    <td>1.0</td>
  </tr>
</table>

