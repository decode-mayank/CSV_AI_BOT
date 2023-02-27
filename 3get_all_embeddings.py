import openai
from openai.embeddings_utils import get_embedding
import pandas as pd
import os
from dotenv import load_dotenv
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def embedding():
    xl = pd.ExcelFile("knowledge_hub.xlsx")
    for sheet_name in xl.sheet_names:
        df = pd.read_excel("knowledge_hub.xlsx",sheet_name=sheet_name)
        df['embedding'] = df['completion'].apply(lambda x: get_embedding(x, engine = 'text-embedding-ada-002'))
        df.to_csv('resmed_embeddings_final.csv', mode='a', index=False, header=not os.path.exists("resmed_embeddings_final.csv"))
        time.sleep(300)

if __name__ == '__main__':
    embedding()