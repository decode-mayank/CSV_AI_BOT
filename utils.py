from datetime import datetime
import time
import os
import csv 

import openai
from openai.embeddings_utils import cosine_similarity
import psycopg2
import pandas as pd
import numpy as np
from products import product, other_products, cheap_products, general_product
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from colors import pr_cyan,pr_bot_response
from debug_utils import debug_steps,debug, debug_attribute

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
my_model = 'text-embedding-ada-002'

DEBUG_CSV = "debug.csv"

RESPONSE_FOR_INVALID_QUERY = "I am a Resmed chatbot, I can't help with that"

GENERAL_QUERY = "General query"
SYMPTOM_QUERY = "Symptom query"
PRODUCT_QUERY = "Product query"
PROGRAM_QUERY = "Program query"

YES = "Yes"
NO = "No"

VERBOSE = os.getenv('VERBOSE')
EXPECTED_SIMILARITY = 0.85


       
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

# Zero shot learning
def call_chat_completion_api(message_log):
    debug("Let's ask Chat completion API to answer user query") 
    bot_response=""
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = message_log,
            max_tokens=150,
            stop=None,
            temperature=0.5,
            stream=True
        )
    pr_bot_response("",end="")
    for chunk in response:
        if "content" in chunk.choices[0].delta.keys():
            bot_response+=chunk.choices[0].delta.content
            pr_cyan(f"{chunk.choices[0].delta.content}",end="")
    print()
    return bot_response
   
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


def identify_answer(user_input, bot_response):
    # Multi shot learning
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"The following is a conversation with an AI assistant. The assistant only answers {YES} or {NO}\n{YES} If the question and answer make sense otherwise say {NO} \nHuman:Q:{user_input},A:{bot_response}\nAI:",
    temperature=0.5,
    max_tokens=10,
    stop=["Human:", "AI:"]
    )
    return response.choices[0].text.strip()

def find_what_user_expects(user_input):
    # Multi shot learning
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Find what user expects from the chatbot system Expected Responses are {GENERAL_QUERY},{SYMPTOM_QUERY},{PRODUCT_QUERY},{PROGRAM_QUERY} \nHuman: I forget a lot and not able to concentrate \nAI:{SYMPTOM_QUERY}\nHuman: Does resmed provide CPAP Products\nAI:{GENERAL_QUERY}\nHuman: I have Mood disruptions, especially anxiety, depression and irritability\nAI:{SYMPTOM_QUERY}\nHuman: How many hours should i sleep daily\nAI:{GENERAL_QUERY}\nHuman:What is the price of CPAP mask\nAI:{PRODUCT_QUERY}\nHuman:Write a program\nAI:{PROGRAM_QUERY}\nHuman:{user_input}",
    temperature=0.5,
    max_tokens=10,
    top_p=1,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text.strip()
  
def find_whether_user_query_is_valid(user_input):
    TOKENS = 100
    # Multi shot learning
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"As an AI assistant specialized in sleep-related topics, I am programmed to provide advice and information only on resmed products, sleep, sleep medicine, mask, snoring, sleep apnea, insomnia and its products, sleep health and ResMed sleep tests and trackers. Please note that I cannot provide information or advice on topics unrelated to the aforementioned sleep-related topics.\nIf you have a question that falls outside of these topics, I will not be able to provide a relevant response. In such cases, please respond with the phrase \"{RESPONSE_FOR_INVALID_QUERY}\"\nPlease note that while I can provide information and advice, my responses should not be considered a substitute for medical advice from a licensed medical professional. If you have any concerns about your sleep health, please consult a medical professional for further guidance.\nPlease generate a response using a maximum of {TOKENS} \nQ: {user_input}\n",
    max_tokens=TOKENS,
    temperature=0.4,
    )
    return response.choices[0].text.strip().replace("A: ","")

def show_products(output):
    prod_response = '\n'
    if(len(output)>0):
        items = output[0]
        debug_attribute("DB Output",output)
        if(len(items)==3):
            pr_cyan("Here are some products, which matches your search")
            for prod, url,price in output:
                products = prod + " - " + url + " - $" + str(price)
                pr_cyan(products)
                prod_response = prod_response + "\n" + products
    return prod_response

def product_query(row,user_input, message_log, bot_response):
    output = general_product(row,user_input)
    if len(output) == 0:
        bot_response += call_chat_completion_api(message_log)
    else:
        bot_response += show_products(output)
    return bot_response

def resmed_chatbot(user_input,message_log,db=True):
    
    MODE = 'w'
    fields = ["user_input","bot_response","level1","level2","level3","level4","level5","level6","db_query"]
    row = []
    row.append(user_input)
    MAX_COLUMNS = len(fields)
    
    if os.path.exists(DEBUG_CSV):
        MODE='a'
    
    # Append user_input 
    message_log.append({"role": "user", "content": user_input})
    
    # Append question mark at end of user_input
    user_input += "?"
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = ""
    
    response_time = 0
    probability = 0
    source = ""
    query_type = ""

    start_time = time.time()
    
    
    response = find_whether_user_query_is_valid(user_input)
    debug_attribute("find_whether_user_query_is_valid",response)

    if(RESPONSE_FOR_INVALID_QUERY not in response):
        # Save embedding vector of the input
        input_embedding_vector = get_embedding(my_model, user_input)

        # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
        df = pd.read_csv('resmed_embeddings_final.csv')
        
        if (len(user_input.split(' '))==1):
            debug_steps(row,"Level 1 - Got a word from user - Prepend What is")
            # If user types single word input then system gets confused so adding what is as a prefix
            user_input= f"What is {user_input}"
            
        query_type = find_what_user_expects(user_input)
        debug_steps(row,"Level 1 - Find what user expects -",query_type)

        debug_attribute("query_type - ",query_type)
        
        if(PROGRAM_QUERY in query_type):
            debug_steps(row,"Level 2 - Found program query - ",query_type)
            pr_bot_response(bot_response)
        elif(GENERAL_QUERY not in query_type):
            debug_steps(row,"Level 2 - It is not a general query -",query_type)
            if 'similarity' in df.columns:
                df['embedding'] = df['embedding'].apply(np.array)
            else:
                df['embedding'] = df['embedding'].apply(eval).apply(np.array)
        
            df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
        
            # Find the highest similarity value in the dataframe column 'similarity'
            highest_similarity = df['similarity'].max()
            debug_attribute("similarity - ",highest_similarity)
                    
            if(highest_similarity >= EXPECTED_SIMILARITY and query_type!=""):
                debug_steps(row,"Level 3 - Found hightest similarity",highest_similarity)
                probability = highest_similarity
                fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
                db_input_or_bot_response = fact_with_highest_similarity.iloc[0]
                show_embedding_answer_to_user = identify_answer(user_input, db_input_or_bot_response)
                debug_steps(row,"Level 4 - Identify embedded output is useful or not - ",show_embedding_answer_to_user)
                debug_attribute("embedded_bot_response - ",db_input_or_bot_response)
                debug_attribute("show_embedding_answer_to_user - ",show_embedding_answer_to_user)
                
                if show_embedding_answer_to_user=="yes":
                    source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
                    bot_response = db_input_or_bot_response
                else:
                    source = ""
                    if "others" == db_input_or_bot_response:
                        debug_steps(row,"Level 5 - Symptoms are common")
                        bot_response = "Your symptoms are more common to define the exact syndrome. can you please provide more detail:"
                        pr_bot_response(bot_response)
                    else:
                        found_symptom = db_input_or_bot_response=="Sleep Apnea" or db_input_or_bot_response=="Insomnia" or db_input_or_bot_response=="Snoring"
                        if (SYMPTOM_QUERY in query_type and found_symptom) or PRODUCT_QUERY in query_type:
                            if(found_symptom):
                                debug_steps(row,"Level 5 - Symptoms found")
                                if db_input_or_bot_response in user_input:
                                    debug_steps(row,"Level 6 - Suggest products")
                                    output = general_product(row,user_input)
                                    print("Here are some products, which matches your search")
                                    bot_response = show_products(output)  
                                else:
                                    debug_steps(row,"Level 6 - Inform sleep disorder and suggest product")
                                    MSG = f"This appears to be a condition called {db_input_or_bot_response}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor."
                                    pr_bot_response(MSG)
                                    SLEEP_ASSESSMENT_INFO="For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'"
                                    pr_cyan(SLEEP_ASSESSMENT_INFO)
                                    bot_response= f"{MSG}\n{SLEEP_ASSESSMENT_INFO}"
                                    output = product(row,db_input_or_bot_response)
                                    bot_response += show_products(output)
                            elif "cheap" in user_input or "cheapest" in user_input:
                                debug_steps(row,"Level 6 - Suggest cheap/ cheapest products")
                                probability = 0
                                if len(outputs)==0:
                                    output = cheap_products(row,user_input)
                                else:
                                    output = cheap_products(row,outputs[-1])
                                show_products(output)
                            elif "Product" == db_input_or_bot_response:
                                debug_steps(row,"Level 6 - Suggest products")
                                output = other_products(row,outputs[-1])
                                bot_response += show_products(output) 
                            else:
                                # debug_steps(f"We are in else part,query_type is {query_type}, bot_response is {bot_response}")
                                debug_steps(row,"Level 6 - Suggest products")
                                bot_response = product_query(row,user_input, message_log, bot_response)
                    outputs.append(bot_response)  
            elif PRODUCT_QUERY in query_type:
                debug_steps(row,"Level 3 - Search product")
                # Let's add dummy rows to fill 4,5,6 levels
                row.extend(["","",""])
                source=""
                bot_response = product_query(row,user_input, message_log, bot_response)                  
            else:
                debug_steps(row,"Level 3 - General query")
                debug(f"It is a general query / similarity {highest_similarity*100} less than {EXPECTED_SIMILARITY*100}")
                bot_response = call_chat_completion_api(message_log)
                outputs.append(bot_response)
    else:
        debug_steps(row,"Level 1 - Query not related to resmed")
        # Looks like user asked query which is not related to resmed
        bot_response=response
        pr_bot_response(bot_response)
        
    if(not bot_response or len(bot_response)<10):
        bot_response=response
        pr_bot_response(bot_response)

    response_time = time.time() - start_time
    
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    # TODO: Find smart way to replace single quote to all string columns
    user_input = user_input.replace("'","''")[:500]
    bot_response = bot_response.replace("'", "''")[:999]
    source = source.replace("'", "''")
    
    if db:
        query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp,source) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}','{source}');"
        debug(f"Query to execute - {query}")
        cur.execute(query)
        conn.commit()
        debug("Data added successfully")
    else:
        debug("DB insert is disabled")
    debug(f"Response time in seconds - {response_time}")
    
    if VERBOSE=="True":
        debug(f"Writing the logs in {DEBUG_CSV}")
        with open(DEBUG_CSV, MODE) as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            if MODE=='w':
                # writing the fields 
                csvwriter.writerow(fields) 
                
            row_length = len(row)
            if(row_length!=MAX_COLUMNS-1):
                dummy_rows_to_add = MAX_COLUMNS-row_length-2
                row.extend(('-'*dummy_rows_to_add).split('-'))
            # writing the data rows 
            row.insert(1,bot_response)
            csvwriter.writerows([row])
    
    # Add the chatbot's response to the conversation history and print it to the console
    message_log.append({"role": "assistant", "content": response})
    
    return bot_response,message_log
