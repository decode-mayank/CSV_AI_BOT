import openai
from openai.embeddings_utils import get_embedding
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


# df = pd.read_csv('scrape_data_with_syed.xlsx')
df = pd.read_excel("3Categories(sleepApnea,sleepHealth,snoring).xlsx",sheet_name="Testing")
df['embedding'] = df['completion'].apply(lambda x: get_embedding(x, engine = 'text-embedding-ada-002'))
df.to_csv('resmed_embeddings.csv')
