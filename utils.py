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

df = pd.read_csv('category_embeddings.csv')

#Color
"""
Initial conversation Bot - Cyan(Dark)
user input - White
Highest probability - Magenta
Bot output - Cyan(Normal)
Violent Answer - Red
Other category - Green

 """

words = ["what", "why", "where", "can",
             "name", "how", "do", "does", 
             "which", "are", "could", "would", 
             "should","whom", "whose", "don't"]


# Calculate embedding vector for the input using OpenAI Embeddings endpoint
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(model, text):
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']

# Save embedding vector of the input

def resmed_chatbot(message_log):
    debug("Clean input from the user")
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = None
    context = ""
    response_time = 0

    start_time = time.time()

    # Save embedding vector of the input
    input_embedding_vector = get_embedding(my_model, input_text)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    debug("Reading category_embedding csv")
    if 'similarity' in df.columns:
        df['embedding'] = df['embedding'].apply(np.array)
    else:
        df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
    debug("Let's find max similarity")
    
    # Find the highest similarity value in the dataframe column 'similarity'
    
    highest_similarity = df['similarity'].max()
    debug(highest_similarity)

    if any(x in input_text.split(' ')[0] for x in words):
        debug("User asked question to our system")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = message_log,
            max_tokens=300,
            stop=None,
            temperature=0.7,
        )
        #print(response)
        bot_response = response["choices"][0]['message']['content']
        print(Fore.CYAN + Style.NORMAL + f"Bot: {bot_response}" + Style.NORMAL)
        probability = 0
        source = ""
       
    elif highest_similarity >= 0.85:
        debug("Found completion which has >=0.85")
        probability = highest_similarity
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        bot_response = fact_with_highest_similarity.iloc[0]
        highest_similarity = df['similarity'].max()
        
        #print(Fore.YELLOW + Style.DIM + f"{df['similarity']}" + Style.NORMAL)
        #print(Fore.MAGENTA + Style.NORMAL + f"{highest_similarity}")

        if "others" == bot_response:
            print("Common Symptom")
            category(bot_response, input_text)
            
      
        else:
            print(Fore.CYAN + Style.NORMAL + "This appears to be a condition called " + f"{bot_response}" + ".It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor.")
            print("For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'")
            category(bot_response, input_text)

            source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
        
            
    # Else pass input to the OpenAI Completions endpoint
    else:
        debug("Let's ask ChatGPT to answer user query")   
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = message_log,
            max_tokens=300,
            stop=None,
            temperature=0.7,
        )
        #print(response)
        bot_response = response['choices'][0]['message']['content']
        print(Fore.CYAN + Style.NORMAL + f"Bot: {bot_response}" + Style.NORMAL)
        probability = 0
       
            

    response_time = time.time() - start_time
    
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql


def category(bot_response, input_text):
    if "others" == bot_response:
        more_detail = (Fore.GREEN + "Your symptoms are more common to define the exact syndrome. can you please provide more detail:")
        print(more_detail)        
    else:
        print(bot_response)      

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
    print(
        Fore.CYAN + Style.BRIGHT + f"Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing." + Style.NORMAL)
    message_log = [
        {"role": "system", "content": "Answer the question only related to the topics of sleep,health,mask from the website https://www.resmed.com.au/knowledge-hub and if you're unsure of the answer, say That I have been trained to answer only sleep and health related queries"}
    ] 

    first_request = True

    while True:
        if first_request:
            input_text = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
            message_log.append({"role": "user", "content": input_text})

            # Add a message from the chatbot to the conversation history
            message_log.append({"role": "assistant", "content": "You are a helpful assistant."})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            #message_log.append({"role": "assistant", "content": response})

            first_request = False

        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            input_text = input(Fore.GREEN + Style.BRIGHT + "User: "+ Style.RESET_ALL)

            # If the user types "quit", end the loop and print a goodbye message
            if input_text.lower() == "quit":
                print("Goodbye!")
                break

            message_log.append({"role": "user", "content": input_text})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

