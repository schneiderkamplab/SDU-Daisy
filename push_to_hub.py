import pandas as pd
from datasets import Dataset

df = pd.read_csv("v_0.2_7_SDU-Culture-1-public.csv", sep=";")
dataset = Dataset.from_pandas(df)

dataset.push_to_hub(
    "schneiderkamplab/SDU-Daisy",
    private=False
)