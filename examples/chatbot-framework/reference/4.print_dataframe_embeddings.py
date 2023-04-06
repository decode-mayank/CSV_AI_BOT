import pandas as pd
import numpy as np

df = pd.read_csv('companies_embeddings.csv')
df['embedding'] = df['embedding'].apply(eval).apply(np.array)
print(df)
