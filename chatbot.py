from datetime import datetime
import time
import os
import csv 

import openai
import pandas as pd
import numpy as np
from products import other_products, cheap_products, general_product
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity

from colors import pr_cyan,pr_bot_response
from debug_utils import debug_steps,debug, debug_attribute
from constants import GENERAL_QUERY,SYMPTOM_QUERY,PRODUCT_QUERY,PROGRAM_QUERY,davinci,turbo
from utils import get_db_connection
from openai_utils import get_embedding
# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
DEBUG_CSV = "debug.csv"

RESPONSE_FOR_INVALID_QUERY = "I am a Resmed chatbot, I can't help with that"

YES = "Yes"
NO = "No"

VERBOSE = os.getenv('VERBOSE')
EXPECTED_SIMILARITY = 0.85

conn,cur = get_db_connection()
# constants

outputs = []

# Zero shot learning
def call_chat_completion_api(row,message_log,query_type,highest_similarity):
    debug("Let's ask Chat completion API to answer user query") 
    PROMPT,MODEL,TOKENS,TEMPERATURE = message_log,turbo,150,0.5
    # bot_response=""
    response = openai.ChatCompletion.create(
            model=MODEL,
            messages = PROMPT,
            max_tokens=TOKENS,
            temperature=TEMPERATURE,
            # stream=True
        )
    
    # TODO: Once everything works fine then switch back to stream
    # pr_bot_response("",end="")
    # for chunk in response:
    #     if "content" in chunk.choices[0].delta.keys():
    #         bot_response+=chunk.choices[0].delta.content
    #         pr_cyan(f"{chunk.choices[0].delta.content}",end="")
    # print()
    
    debug_steps(row,f'Level 3 - Query type is {query_type} / similarity {highest_similarity*100} less than {EXPECTED_SIMILARITY*100} {call_chat_completion_api.__name__} - {response}, Additional information: Model-{MODEL}, Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE}, PROMPT-{PROMPT}"')
    pr_bot_response(response)
    return response

def find_what_user_expects(row,user_input):
    # Multi shot learning
    PROMPT,TOKENS,TEMPERATURE,MODEL,STOP = f"Find what user expects from the chatbot system Expected Responses are {GENERAL_QUERY},{SYMPTOM_QUERY},{PRODUCT_QUERY},{PROGRAM_QUERY} \nHuman: I forget a lot and not able to concentrate \nAI:{SYMPTOM_QUERY}\nHuman: Does resmed provide CPAP Products\nAI:{GENERAL_QUERY}\nHuman: I have Mood disruptions, especially anxiety, depression and irritability\nAI:{SYMPTOM_QUERY}\nHuman: How many hours should i sleep daily\nAI:{GENERAL_QUERY}\nHuman:What is the price of CPAP mask\nAI:{PRODUCT_QUERY}\nHuman:Write a program\nAI:{PROGRAM_QUERY}\nHuman:{user_input}",10,0.5,davinci,[" Human:", " AI:"]
    response = openai.Completion.create(
    model=MODEL,
    prompt=PROMPT,
    temperature=TEMPERATURE,
    max_tokens=TOKENS,
    stop=STOP
    )
    debug_steps(row,f"Level 1 - {find_what_user_expects.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},STOP-{STOP},PROMPT-{PROMPT}")
    
    return response.choices[0].text.strip()
  
def find_whether_user_query_is_valid(row,user_input):
    TOKENS,TEMPERATURE,MODEL =100,0.4,davinci
    PROMPT = f"As an AI assistant specialized in sleep-related topics, I am programmed to provide advice and information only on resmed products, sleep, sleep medicine, mask, snoring, sleep apnea, insomnia and its products, sleep health and ResMed sleep tests and trackers. Please note that I cannot provide information or advice on topics unrelated to the aforementioned sleep-related topics.\nIf you have a question that falls outside of these topics, I will not be able to provide a relevant response. In such cases, please respond with the phrase \"{RESPONSE_FOR_INVALID_QUERY}\"\nPlease note that while I can provide information and advice, my responses should not be considered a substitute for medical advice from a licensed medical professional. If you have any concerns about your sleep health, please consult a medical professional for further guidance.\nPlease generate a response using a maximum of {TOKENS} \nQ: {user_input}\n",
    # Multi shot learning
    response = openai.Completion.create(
    model=MODEL,
    prompt=PROMPT,
    max_tokens=TOKENS,
    temperature=TEMPERATURE,
    )
    
    debug_steps(row,f"Level 1 - {find_whether_user_query_is_valid.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},PROMPT-{PROMPT}")
    return response.choices[0].text.strip().replace("A: ","")

def identify_answer(row,user_input, bot_response):
    # Multi shot learning
    PROMPT,TOKENS,TEMPERATURE,MODEL,STOP = f"The following is a conversation with an AI assistant. The assistant only answers {YES} or {NO}\n{YES} If the question and answer make sense otherwise say {NO} \nHuman:Q:{user_input},A:{bot_response}\nAI:",10,0.5,davinci,["Human:", "AI:"]
    response = openai.Completion.create(
    model=davinci,
    prompt=PROMPT,
    temperature=TEMPERATURE,
    max_tokens=TOKENS,
    stop=STOP
    )
    debug_steps(row,f"Level 4 - {identify_answer.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},PROMPT-{PROMPT}")
    return response.choices[0].text.strip()

def show_products(output):
    prod_response = '\n'
    if(len(output)>0):
        items = output[0]
        output = output if len(output)==1 else output[0:2]
        debug_attribute("DB Output",output)
        if(len(items)==3):
            pr_cyan("Here are some products, which matches your search")
            for prod, url,price in output:
                products = prod + " - " + url + " - $" + str(price)
                pr_cyan(products)
                prod_response = prod_response + "\n" + products
    return prod_response

def product_query(row,user_input, bot_response):
    output = general_product(row,user_input)
    if len(output) == 0:
        bot_response = "Unable to find products in DB"
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
    # If user types single word input then system gets confused so adding what is as a prefix
    if (len(user_input.split(' '))==1):
        user_input = f"What is {user_input}"
            
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response_accepted = True
    bot_response = ""
    
    response_time = 0
    probability = 0
    source = ""
    query_type = ""

    start_time = time.time()
    
    
    response = find_whether_user_query_is_valid(row, user_input)
    debug_attribute("find_whether_user_query_is_valid",response)

    if(RESPONSE_FOR_INVALID_QUERY not in response):
        # Save embedding vector of the input
        input_embedding_vector = get_embedding(user_input)

        # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
        df = pd.read_csv('resmed_embeddings_final.csv')
                    
        query_type = find_what_user_expects(row,user_input)

        debug_attribute("query_type - ",query_type)
        
        if(PROGRAM_QUERY in query_type):
            debug_steps(row,"Level 3 - Found program query - ",query_type)
            pr_bot_response(bot_response)
        if(GENERAL_QUERY not in query_type):
            debug_steps(row,"Level 3 - It is not a general query -",query_type)
            if 'similarity' in df.columns:
                df['embedding'] = df['embedding'].apply(np.array)
            else:
                df['embedding'] = df['embedding'].apply(eval).apply(np.array)
        
            df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))
        
            # Find the highest similarity value in the dataframe column 'similarity'
            highest_similarity = df['similarity'].max()
            debug_attribute("similarity - ",highest_similarity)
                    
            if(highest_similarity >= EXPECTED_SIMILARITY and query_type!=""):
                debug_steps(row,"Level 4 - Found highest similarity",highest_similarity)
                probability = highest_similarity
                fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
                db_input_or_bot_response = fact_with_highest_similarity.iloc[0]
                
                
                found_symptom = db_input_or_bot_response=="Sleep Apnea" or db_input_or_bot_response=="Insomnia" or db_input_or_bot_response=="Snoring"
                if (SYMPTOM_QUERY in query_type):
                    if(found_symptom):
                        source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
                        debug_steps(row,f"Level 5 - {SYMPTOM_QUERY},found symptom & suggest products")
                        MSG = f"This appears to be a condition called {db_input_or_bot_response}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor."
                        pr_bot_response(MSG)
                        SLEEP_ASSESSMENT_INFO="For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'"
                        pr_cyan(SLEEP_ASSESSMENT_INFO)
                        bot_response= f"{MSG}\n{SLEEP_ASSESSMENT_INFO}"
                    else:
                        debug_steps(row,f"Level 5 - {SYMPTOM_QUERY}, Symptoms are common")
                        bot_response = "Your symptoms are more common to define the exact syndrome. can you please provide more detail:"
                        pr_bot_response(bot_response)
                 
                elif(PRODUCT_QUERY in query_type):
                    if "cheap" in user_input or "cheapest" in user_input:
                        probability = 0
                        if len(outputs)==0:
                            output = cheap_products(row,user_input)
                        else:
                            output = cheap_products(row,outputs[-1])
                        show_products(output)
                    elif "Products" == db_input_or_bot_response:
                        source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
                        output = other_products(row,outputs[-1])
                        bot_response += show_products(output) 
                    else:
                        bot_response = product_query(row,user_input, bot_response)
                else:                   
                    show_embedding_answer_to_user = identify_answer(row, user_input, db_input_or_bot_response)
                    debug_attribute("embedded_bot_response - ",db_input_or_bot_response)
                    debug_attribute("show_embedding_answer_to_user - ",show_embedding_answer_to_user)
                
                    if show_embedding_answer_to_user=="yes":
                        debug("Level 6 - Show embedding answer to user")
                        source = df.loc[df['similarity'] == highest_similarity, 'prompt'].iloc[0]
                        bot_response = db_input_or_bot_response
                    else:
                        source = "" 
                        debug("Level 6 - Don't show embedding answer")                
            else:
                bot_response = call_chat_completion_api(row,message_log,query_type,highest_similarity)
                outputs.append(bot_response)
    else:
        debug_steps(row,"Level 2 - Query not related to resmed")
        # Looks like user asked query which is not related to resmed
        bot_response=response
        pr_bot_response(bot_response)
        
    if(not bot_response or len(bot_response)<10):
        debug_steps(row,f"Level ??? - bot_response is not useful so, let's use response from {find_whether_user_query_is_valid.__name__}")
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
