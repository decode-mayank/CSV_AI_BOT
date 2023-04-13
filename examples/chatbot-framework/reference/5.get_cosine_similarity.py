import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

my_model = 'text-embedding-ada-002'
my_input = 'This is fact about company XYM'


def get_embedding(model: str, text: str) -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']


input_embedding_vector = get_embedding(my_model, my_input)

df = pd.read_csv('companies_embeddings.csv')
df['embedding'] = df['embedding'].apply(eval).apply(np.array)
df['similarity'] = df['embedding'].apply(
    lambda x: cosine_similarity(x, input_embedding_vector))
print(df)
