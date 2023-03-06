from datetime import datetime
import time
import openai
from openai.embeddings_utils import cosine_similarity
import os
import psycopg2

import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# Get db connections
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database=os.getenv('DB'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    return conn


# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
my_model = 'text-embedding-ada-002'

inputs, outputs = [], []


conn = get_db_connection()
cur = conn.cursor()


#Color
"""
Initial conversation Bot - Cyan(Dark)
user input - White
List of probability - Yellow(Dim)
Highest probability - Magenta
Bot output - Cyan(Normal)
Violent Answer - Red
Other category - Green

 """

words = ["what", "why", "when", "where", 
             "name", "is", "how", "do", "does", 
             "which", "are", "could", "would", 
             "should", "has", "have", "whom", "whose", "don't"]


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
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = None
    context = ""
    response_time = 0

    if (not (user_input)):
        user_input = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)

    start_time = time.time()
    context = context + user_input

    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, user_input)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    df = pd.read_csv('category_embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
    

    # Find the highest similarity value in the dataframe column 'similarity'
    highest_similarity = df['similarity'].max()
    if any(x in user_input.split(' ')[0] for x in words):
        prompt = user_input
        if inputs and len(inputs) > 0 and len(outputs) > 0:
            last_input = inputs[-1]
            last_output = outputs[-1]
            prompt = f"{user_input} (based on my previous question: {last_input}, and your previous answer: {last_output})"
        response = openai.Completion.create(
            prompt=prompt+"Answer the question only related to the topics of sleep,health,mask and if you're unsure of the answer, say That I have been trained to answer only sleep and health related queries",
            temperature=0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="text-davinci-003"
        )
        bot_response = response["choices"][0]["text"].replace('.\n', '')
        print(Fore.CYAN + Style.NORMAL + f"Bot: {bot_response}" + Style.NORMAL)
        probability = 0
        source = ""
       

    elif highest_similarity >= 0.85:
        probability = highest_similarity
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response = fact_with_highest_similarity.iloc[0]
        #print(Fore.YELLOW + Style.DIM + f"{df['similarity']}" + Style.NORMAL)
        print(Fore.MAGENTA + Style.NORMAL + f"{highest_similarity}")
        if "others" == bot_response:
            print("Common Symptom")
            category(bot_response, user_input)
        else:
            print(Fore.CYAN + Style.NORMAL + "This appears to be a condition called " + f"{bot_response}" + ".It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor.")
            category(bot_response, user_input)
            source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
        
            
    # Else pass input to the OpenAI Completions endpoint
    else:
        prompt = user_input
        if inputs and len(inputs) > 0 and len(outputs) > 0:
            last_input = inputs[-1]
            last_output = outputs[-1]
            prompt = f"{user_input} (based on my previous question: {last_input}, and your previous answer: {last_output})"
        response = openai.Completion.create(
            prompt=prompt+"Answer the question only related to the topics of sleep,health,mask and if you're unsure of the answer, say That I have been trained to answer only sleep and health related queries",
            temperature=0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="text-davinci-003"
        )
        outputs.append(bot_response)
        bot_response = response["choices"][0]["text"].replace('.\n', '')
        print(Fore.CYAN + Style.NORMAL + f"Bot: {bot_response}" + Style.NORMAL)
        probability = 0
        source = ""
       
            

    response_time = time.time() - start_time
    
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    user_input = user_input.replace("'","''")
    #bot_response = bot_response.replace("'", "''")
    #query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp,source) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}','{source}');"
    #print(f"Query to execute - {query}")
    #cur.execute(query)
    #conn.commit()
    # print("Data added successfully")
    return bot_response


def category(bot_response, user_input):
    if "others" == bot_response:
        more_detail = (Fore.GREEN + "Your symptoms are more common to define the exact syndrome. can you please provide more detail:")
        print(more_detail)
        user = input(Fore.GREEN + Style.BRIGHT + "Users: " + Style.RESET_ALL)
        resmed_chatbot(user + user_input)
    
    else:
        print(bot_response)
        outputs.append(bot_response)
                  

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
