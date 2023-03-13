from datetime import datetime
import time
import openai
from openai.embeddings_utils import cosine_similarity
import os
import psycopg2

import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from products import product, other_products, cheap_products
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
my_model = 'text-embedding-ada-002'



def debug(msg):
    verbose=os.getenv('VERBOSE')
    if verbose=="True":
        print(msg)  
        
# Get db connections
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database=os.getenv('DB'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    return conn


conn = get_db_connection()
cur = conn.cursor()

outputs = []
words = ["what", "why", "where", "can",
             "name", "how", "do", "does", 
             "which", "are", "could", "would", 
             "should","whom", "whose", "don't", "list", "tell", "give"]

def call_chat_completion_api(message_log):
    bot_response=""
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = message_log,
            max_tokens=200,
            stop=None,
            temperature=0.7,
            stream=True
        )
    print(f"{Fore.CYAN}{Style.NORMAL}Bot: {Style.NORMAL}",end="")
    for chunk in response:
        if "content" in chunk.choices[0].delta.keys():
            bot_response+=chunk.choices[0].delta.content
            print(Fore.CYAN + Style.NORMAL + f"{chunk.choices[0].delta.content}" + Style.NORMAL,end="")
    print()
    return bot_response
   
def get_category(bot_response):
    if "others" == bot_response:
        more_detail = (Fore.GREEN + "Your symptoms are more common to define the exact syndrome. can you please provide more detail:")
        print(more_detail)            

# Calculate embedding vector for the input using OpenAI Embeddings endpoint
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(model, text):
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']


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
     
     
def resmed_chatbot(user_input,message_log):
    debug("Clean input from the user")
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = None
    response_time = 0
    probability = 0
    source = ""

    start_time = time.time()

    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, user_input)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    debug("Reading category_embedding csv")
    
    df = pd.read_csv('resmed_embeddings_final.csv')
    
    
    # If user types single word input then system gets confused so adding what is as a prefix
    if (len(user_input.split(' '))==1):
        user_input= f"What is {user_input}"
        
    if len(user_input.split(' '))<4:
        # If we get user input with lesser words length of 4 then drop the rows where url is null
        df = df[df["url"].notnull()]

    if 'similarity' in df.columns:
        df['embedding'] = df['embedding'].apply(np.array)
    else:
        df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
    debug("Let's find max similarity")
    
    # Find the highest similarity value in the dataframe column 'similarity'
    
    highest_similarity = df['similarity'].max()
    debug(highest_similarity)
    if highest_similarity >= 0.82:
        debug("Found completion which has >=0.85")
        probability = highest_similarity
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response = fact_with_highest_similarity.iloc[0]
        highest_similarity = df['similarity'].max()
        
        if "others" == bot_response:
            debug("Common Symptom")
            get_category(bot_response)

        elif "Product" == bot_response:
            output = other_products(outputs[-1])
            for prod, url in output:
                products = prod + " - " + url
                print(Fore.CYAN + Style.NORMAL + f"{products}" + Style.NORMAL)
                bot_response = bot_response + "\n" + products
        else:
            if "product" in user_input or "products" in user_input.lower():
                output = product(bot_response)
            elif any(x in user_input.split(' ')[0] for x in words):
                debug("User asked question to our system")
                bot_response = call_chat_completion_api(message_log)
            elif(bot_response=="sleep apnea" or bot_response=="insomnia" or bot_response=="snoring"):
                print(f"{Fore.CYAN} {Style.NORMAL} EmbeddedBot: This appears to be a condition called {bot_response}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor.")
                print("For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'")
                get_category(bot_response)
            outputs.append(bot_response)
            output = product(bot_response)
            source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
            print("Here are some products, which matches your search")
            for prod, url in output:
                products = prod + " - " + url
                print(Fore.CYAN + Style.NORMAL + f"{products}" + Style.NORMAL)
                bot_response = bot_response + "\n" + products
    elif any(x in user_input.split(' ')[0] for x in words):
        debug("User asked question to our system")
        bot_response = call_chat_completion_api(message_log)

    elif "cheap" in user_input or "cheapest" in user_input:
        probability = 0
        source = ""
        output = cheap_products(outputs[-1])
        for prod, url in output:
            bot_response = prod + " - " + url
            print(Fore.CYAN + Style.NORMAL + f"Cheapest option: {bot_response}" + Style.NORMAL)

    # Else pass input to the OpenAI Chat Completion endpoint
    else:
        debug("Let's ask ChatGPT to answer user query")  
        bot_response = call_chat_completion_api(message_log)
    response_time = time.time() - start_time
    
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    user_input = user_input.replace("'","''")
    bot_response = bot_response.replace("'", "''")
    query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp,source) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}','{source}');"
    debug(f"Query to execute - {query}")
    cur.execute(query)
    conn.commit()
    debug("Data added successfully")
    return bot_response
