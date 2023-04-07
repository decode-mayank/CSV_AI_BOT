import openai
from openai.embeddings_utils import get_embedding
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv('companies.csv')
df['embedding'] = df['content'].apply(lambda x: get_embedding(x, engine = 'text-embedding-ada-002'))
df.to_csv('companies_embeddings.csv')
