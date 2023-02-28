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
from colorama import Fore, Back, Style
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# Insert your API key
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

# Get db connections
conn = get_db_connection()
cur = conn.cursor()
inputs, outputs = [], []

# Calculate embedding vector for the input using OpenAI Embeddings endpoint
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(model, text):
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']


# Save embedding vector of the input
def resmed_chatbot(user_input, inputs=[]):
    
    time_stamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted=True
    bot_response = None
    context=""
    response_time = 0
    
    
    if(not(user_input)):
      user_input = input(f"{Fore.GREEN}{Style.BRIGHT}User: {Style.RESET_ALL}")

    start_time = time.time()
    context = context + user_input
    
    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, user_input)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    df = pd.read_csv('resmed_embeddings_final.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))

    # Find the highest similarity value in the dataframe column 'similarity'
    highest_similarity = df['similarity'].max()

    # If the highest similarity value is equal or higher than 0.8 then print the 'completion' with the highest similarity
    if highest_similarity >= 0.8:
        probability = highest_similarity
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response = fact_with_highest_similarity.iloc[0]
        outputs.append(bot_response)
        
    # Else pass input to the OpenAI Completions endpoint
    else:
        prompt = f"Answer the question only related to the topics of sleep,health,mask and if you're unsure of the answer, say That I have been trained to answer only sleep and health related queries"
        if inputs and len(inputs) > 0 and len(outputs)>0:
            last_input = inputs[-1]
            last_output = outputs[-1]
            prompt += f"(based on my previous question: {last_input}, and your previous answer: {last_output})"
        response = openai.Completion.create(
            prompt= f"{prompt} {user_input}?",
            temperature=0,
            max_tokens=50,
            model="text-davinci-003"
        )
        bot_response = response['choices'][0]['text'].replace('\n', '')
        probability = 0
    
    response_time = time.time() - start_time
    print(Fore.CYAN + Style.BRIGHT + f"Bot: {bot_response}" + Style.NORMAL)
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    user_input = user_input.replace("'","''")
    bot_response = bot_response.replace("'","''")
    query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}');"
    print(f"Query to execute - {query}")
    cur.execute(query)
    conn.commit()
    print("Data added successfully")
    return bot_response


def get_moderation(question):
    """
    Check the question is safe to ask the model
    Parameters:
        question (str): The question to check
    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None
    
if __name__ == '__main__':
  print(Fore.CYAN + Style.BRIGHT + f"Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing." + Style.NORMAL)
  while True:
    input_text = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
    inputs.append(input_text)
    errors = get_moderation(input_text)
    if errors:
        print(
            Fore.RED 
            + Style.BRIGHT
            + "Sorry, you're question didn't pass the moderation check:"
        )
        for error in errors:
            print(error)
        print(Style.RESET_ALL)
        continue
    resmed_chatbot(input_text, inputs)