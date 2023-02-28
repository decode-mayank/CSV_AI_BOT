import os
import time

import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

INPUT_FILE_NAME = "knowledge_hub.csv"
OUTPUT_FILE_NAME = "resmed_embeddings_final.csv"
TIME_TO_SLEEP = 30 # seconds


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def embedding():
    df2=pd.DataFrame()
    df2_length=0
    df1 = pd.read_csv(INPUT_FILE_NAME)
    try:
        df2 = pd.read_csv(OUTPUT_FILE_NAME)
        df2_length= len(df2)
    except FileNotFoundError:
        pass
    
    if(df2_length==len(df1)):
        print(f"Embeddings already completed")
    else:
        if(df2_length!=0):
            print(f"Embedding completed for {df2_length} rows. So, let's skip {df2_length} rows")
            df1= df1[df2_length:]
        else:
            print("Embeddings not yet started")
            print(f"{OUTPUT_FILE_NAME} file has {df2_length} rows")
            
        chunks_count = len(df1)/8
        chunks = np.array_split(df1, chunks_count)
        print(f"Chunks length {len(chunks)}")

        for index,chunk in enumerate(chunks,start=1):
            chunk['embedding'] = chunk['completion'].apply(lambda x: get_embedding(x, engine = 'text-embedding-ada-002'))
            chunk.to_csv(OUTPUT_FILE_NAME, mode='a', index=False, header=not os.path.exists(OUTPUT_FILE_NAME))
            print(f"Completed Chunk {index}, processed {len(chunk)} rows")
            print(f"Sleeping {TIME_TO_SLEEP} seconds")
            time.sleep(TIME_TO_SLEEP)
            

if __name__ == '__main__':
    print(f"If we scraped new datas, then delete file {OUTPUT_FILE_NAME} and run this script")
    embedding()