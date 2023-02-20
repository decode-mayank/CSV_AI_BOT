# Imports
import os
import time
from datetime import datetime

import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import psycopg2
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
probability = 0

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database=os.getenv('DB'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    return conn
  

# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'

context = ""
conn = get_db_connection()
cur = conn.cursor()

# Calculate embedding vector for the input using OpenAI Embeddings endpoint
def get_embedding(model,text):
      result = openai.Embedding.create(
        model = model,
        input = text
      )
      return result['data'][0]['embedding']

def get_content(user_input=None):
    time_stamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted=True
    bot_response = None
    context=""
    response_time = 0


    if(not(user_input)):
      user_input = input("User: ")

    start_time = time.time()
    context = context + user_input
    
    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, user_input)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    df = pd.read_csv('resmed_embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))

    print(df["similarity"])
    # Find the highest similarity value in the dataframe column 'similarity'
    highest_similarity = df['similarity'].max()

    # If the highest similarity value is equal or higher than 0.9 then print the 'completion' with the highest similarity
    if highest_similarity >= 0.8:
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response=fact_with_highest_similarity.iloc[0]
        probability = highest_similarity
        
    # Else pass input to the OpenAI Completions endpoint
    else:
        response = openai.Completion.create(
          model = 'text-davinci-003',
          prompt = user_input,
          max_tokens = 100,
          temperature = 0
        )
        bot_response = response['choices'][0]['text'].replace('\n', '')
        probability = 0
        
    response_time = time.time() - start_time
    print(bot_response)
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    bot_response = bot_response.replace("'","''")
    query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}');"
    print(f"Query to execute - {query}")
    cur.execute(query)
    conn.commit()
    print("Data added successfully")
    return bot_response

if __name__ == '__main__':
  while True:
    get_content()
