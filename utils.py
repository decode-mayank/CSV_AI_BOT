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


GENERAL_QUERY = "General query"
SYMPTOM_QUERY = "Symptom query"
PRODUCT_QUERY = "Product query"

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
    debug("Let's ask ChatGPT to answer user query") 
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
    
def find_what_user_expects(user_input):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Find what user expects from the chatbot system Expected Responses are {GENERAL_QUERY},{SYMPTOM_QUERY},{PRODUCT_QUERY} \nHuman: I forget a lot and not able to concentrate \nAI:{SYMPTOM_QUERY}\nHuman: Does resmed provide CPAP Products\nAI:{GENERAL_QUERY}\nHuman: I have Mood disruptions, especially anxiety, depression and irritability\nAI:{SYMPTOM_QUERY}\nHuman: How many hours should i sleep daily\nAI:{GENERAL_QUERY}\nHuman:What is the price of CPAP mask\nAI:{PRODUCT_QUERY}\nHuman:{user_input}",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text.strip()
 
     
def resmed_chatbot(user_input,message_log):
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = None
    response_time = 0
    probability = 0
    source = ""
    query_type = ""

    start_time = time.time()

    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, user_input)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    df = pd.read_csv('resmed_embeddings_final.csv')
    
    # If user types single word input then system gets confused so adding what is as a prefix
    if (len(user_input.split(' '))==1):
        user_input= f"What is {user_input}"
    else:
        query_type = find_what_user_expects(user_input)

    if 'similarity' in df.columns:
        df['embedding'] = df['embedding'].apply(np.array)
    else:
        df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
    
    # Find the highest similarity value in the dataframe column 'similarity'
    highest_similarity = df['similarity'].max()
    debug(f"Max similarity - {highest_similarity}")
    
    if(GENERAL_QUERY not in query_type and highest_similarity >= 0.82):
        probability = highest_similarity
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response = fact_with_highest_similarity.iloc[0]
        debug(f"We are inside if and query_type is {query_type}, bot_response is {bot_response}, similarity is {highest_similarity}")
        
        if "others" == bot_response:
            debug("Common Symptom")
            get_category(bot_response)

        found_symptom = bot_response=="Sleep Apnea" or bot_response=="Insomnia" or bot_response=="Snoring"
        if (SYMPTOM_QUERY in query_type and found_symptom) or PRODUCT_QUERY in query_type:
            if(found_symptom):
                print(f"{Fore.CYAN} {Style.NORMAL} EmbeddedBot: This appears to be a condition called {bot_response}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor.")
                print("For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'")
                
            if "Product" == bot_response:
                output = other_products(outputs[-1])
                for prod, url in output:
                    products = prod + " - " + url
                    print(Fore.CYAN + Style.NORMAL + f"{products}" + Style.NORMAL)
                    bot_response = bot_response + "\n" + products                   
                get_category(bot_response)
                outputs.append(bot_response)
                output = product(bot_response)
                source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
                print("Here are some products, which matches your search")
                for prod, url in output:
                    products = prod + " - " + url
                    print(Fore.CYAN + Style.NORMAL + f"{products}" + Style.NORMAL)
                    bot_response = bot_response + "\n" + products

            elif "cheap" in user_input or "cheapest" in user_input:
                probability = 0
                source = ""
                output = cheap_products(outputs[-1])
                for prod, url in output:
                    bot_response = prod + " - " + url
                    print(Fore.CYAN + Style.NORMAL + f"Cheapest option: {bot_response}" + Style.NORMAL)
    else:
        debug(f"We are in else part,query_type is {query_type}, bot_response is {bot_response}")
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
