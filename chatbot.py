from datetime import datetime
import time
import os
import csv 

import openai
import pandas as pd
import numpy as np
from products import product, other_products, cheap_products, general_product
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity

from colors import pr_cyan,pr_bot_response
from debug_utils import debug_steps,debug, debug_attribute
from constants import GENERAL_QUERY,SYMPTOM_QUERY,PRODUCT_QUERY,PROGRAM_QUERY,GENERAL_PRODUCT_QUERY,davinci,turbo,babbage,SEPARATORS
from utils import get_db_connection
from openai_utils import get_embedding
# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
DEBUG_CSV = "debug.csv"

RESPONSE_FOR_INVALID_QUERY = "I am a Resmed chatbot, I can't help with that"
UNABLE_TO_FIND_PRODUCTS_IN_DB = "Unable to find products in DB"

YES = "Yes"
NO = "No"

VERBOSE = os.getenv('VERBOSE')
EXPECTED_SIMILARITY = 0.85

conn,cur = get_db_connection()
# constants

outputs = []

# Zero shot learning
def call_chat_completion_api(row,message_log,level):
    debug("Let's ask Chat completion API to answer user query") 
    PROMPT,MODEL,TOKENS,TEMPERATURE = message_log,turbo,150,0
    # bot_response=""
    response = openai.ChatCompletion.create(
            model=MODEL,
            messages = PROMPT,
            max_tokens=TOKENS,
            temperature=TEMPERATURE
            # stream=True
        )
    
    # TODO: Once everything works fine then switch back to stream
    # pr_bot_response("",end="")
    # for chunk in response:
    #     if "content" in chunk.choices[0].delta.keys():
    #         bot_response+=chunk.choices[0].delta.content
    #         pr_cyan(f"{chunk.choices[0].delta.content}",end="")
    # print()
    
    # Query type is {query_type} / similarity {highest_similarity*100} less than {EXPECTED_SIMILARITY*100}
    debug_steps(row,f'{level} - {call_chat_completion_api.__name__} - {response}, Additional information: Model-{MODEL}, Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE}, PROMPT-{PROMPT}"',level)
    return response.choices[0].message.content.strip()

def get_answer_from_gpt(row,prompt,level):
    # Multi shot learning
    TOKENS,TEMPERATURE,MODEL,STOP = 200,0,davinci,[" Human:", " AI:"]
    response = openai.Completion.create(
    model=MODEL,
    # prompt="""
    # ResMed is a global leader in developing and manufacturing medical devices and software solutions for the diagnosis, treatment, and management of sleep apnea, chronic obstructive pulmonary disease (COPD), and other respiratory conditions. ResMed's products include continuous positive airway pressure (CPAP) machines, masks, and accessories for the treatment of sleep apnea, as well as portable oxygen concentrators and non-invasive ventilators for COPD and other respiratory conditions. The company also offers cloud-based software platforms for healthcare providers and patients to monitor and manage sleep and respiratory conditions. More about resmed at https://www.resmed.co.in/
    # You are resmed intelligent chatbot designed to identify the intent and most likely cause of their symptoms and help individuals with information on Resmed's services and products, providing them advice on how to improve their sleep quality. 

    # Instructions: 
    # - Only answer questions related to sleep, sleep medicine, mask, snoring, sleep apnea, insomnia, ResMed products, sleep health, and ResMed sleep tests and trackers.  Along with the answers provide intent, entity and suggest resmed products
    # - If you're unsure of an answer, you can say I am a Resmed chatbot, I can't help with that

    # Human: is CPAP safe to use
    # AI: Yes, CPAP is a safe and effective treatment for sleep apnea. It is designed to provide a steady stream of air pressure to keep your airway open while you sleep. The air pressure is adjusted to your individual needs and monitored by your doctor. ResMed offers a range of CPAP masks and machines to help you get the best possible sleep. Intent: CPAP Safe, Entity: CPAP, Suggested Product: ResMed CPAP masks and machines.

    # Human: what is python
    # AI:
    # """,
    prompt=prompt,
    temperature=TEMPERATURE,
    max_tokens=TOKENS,
    stop=STOP
    )
    
    debug_steps(row,f"{level} - {get_answer_from_gpt.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},STOP-{STOP},PROMPT-{prompt}",level)
    
    return response.choices[0].text.strip()


def find_what_user_expects(row,user_input,level):
    # Multi shot learning
    PROMPT,TOKENS,TEMPERATURE,MODEL,STOP = f"Find what user expects from the chatbot system Expected Responses are {GENERAL_QUERY},{SYMPTOM_QUERY},{GENERAL_PRODUCT_QUERY},{PRODUCT_QUERY},{PROGRAM_QUERY} H:do you sell mask A:{GENERAL_QUERY},{GENERAL_PRODUCT_QUERY},H: I forget a lot and not able to concentrate A:{SYMPTOM_QUERY} H: Does resmed provide CPAP Products A:{GENERAL_QUERY} H: I have Mood disruptions, especially anxiety, depression and irritability A:{SYMPTOM_QUERY} H: How many hours should i sleep daily A:{GENERAL_QUERY} H:What is the price of CPAP mask AI:{PRODUCT_QUERY} H:Write a program A:{PROGRAM_QUERY} H:do you also sell cushion A:{GENERAL_PRODUCT_QUERY} H:{user_input} A:",10,0,davinci,[" H:", " A:"]
    response = openai.Completion.create(
    model=MODEL,
    prompt=PROMPT,
    temperature=TEMPERATURE,
    max_tokens=TOKENS,
    stop=STOP
    )
    
    debug_steps(row,f"{level} - {find_what_user_expects.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},STOP-{STOP},PROMPT-{PROMPT}",level)
    
    return response.choices[0].text.strip()

def show_products(output):
    prod_response = '\n'
    if(len(output)>0):
        items = output[0]
        output = output if len(output)==1 else output[0:2]
        debug_attribute("DB Output",output)
        if(len(items)==3):
            pr_cyan(f"Here are some products, which matches your search {output}")
            for prod, url,price in output:
                products = prod + " - " + url + " - $" + str(price)
                prod_response += products + "\n"
    return prod_response

def product_query(row,user_input, bot_response,level):
    output = general_product(row,user_input,level)
    if len(output) == 0:
        bot_response = UNABLE_TO_FIND_PRODUCTS_IN_DB
    else:
        bot_response += show_products(output)
    return bot_response

def identify_symptom(user_input):
    TOKENS = 100
    # Multi shot learning
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Snoring, sleep apnea, and insomnia are all different sleep disorders with distinct symptoms and causes. Here are some differences that may help you differentiate between the three:Snoring:Characterized by loud, rhythmic breathing sounds during sleep,Usually harmless, although it can still disrupt your sleep or your partner's sleep Typically caused by a partial obstruction in the airway, often due to relaxed muscles in the throat or nasal congestion,Usually associated with pauses in breathing or gasping sensations during sleep,Change in the level of attention, concentration, or memory.Sleep apnea:Characterized by pauses in breathing or shallow breaths during sleep,Often accompanied by loud snoring and gasping or choking sensations during sleep,Can lead to excessive daytime sleepiness,Being Overweight(adds fat around the neck and airway),Having inflamed tonsils and adenoids,Having blocked nose due to allergy or cold,Structural problem with shape of the nose, neck or jaw,Frequently urinating at night,Waking up with night sweats,High blood pressure,Mood swings,Impotence and reduced sex drive.Insomnia:A sleep disorder characterized by difficulty falling asleep,staying asleep,or waking up too early in the morning,Often associated with anxiety, stress, or other psychological factors, as well as medical conditions or medications,Can lead to excessive daytime sleepiness, fatigue, irritability, difficulty concentrating, and other health problems,Making more mistakes or having accidents,Feel tired or sleepy during the day.Extract Sleep disorder from user input.Q: Sore throat on awakening A: Snoring Q: Excessive daytime sleepiness A: Snoring Q:I have fever A: Not a sleep disorder Q: Mood Swings A: Sleep Apnea Q: Difficulty staying asleep A: Insomnia Q:{user_input}",
    max_tokens=TOKENS,
    temperature=0,
    )
    return response.choices[0].text.strip().replace("A: ","")

def get_products(row,query_type,user_input,bot_response):
    prod_response=""
    debug_steps(row,f"{query_type}",level=3)
    if "cheap" in user_input or "cheapest" in user_input:
        if len(outputs)==0:
            output = cheap_products(row,user_input,level=3)
        else:
            output = cheap_products(row,outputs[-1],level=3)
        prod_response += show_products(output)
    else:
        prod_response += product_query(row,user_input, bot_response,level=3)
    return prod_response
    
def resmed_chatbot(user_input,message_log,db=True):
    MODE = 'w'
    fields = ["user_input","bot_response","level1","level2","level3","level4","level5","level6","level7"]
    MAX_COLUMNS = len(fields)
    row = [""] * MAX_COLUMNS
    row[0] = user_input
    
    debug_steps(row,f"Message log - {message_log}",level=7)
    
    if os.path.exists(DEBUG_CSV):
        MODE='a'
    
    # Append user_input 
    prompt=f"{message_log}Human:{user_input}\nAI:"
    prompt = prompt.replace(SEPARATORS,'')
    
    # Append question mark at end of user_input
    # user_input += "?"
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
        

    response_from_resmed = get_answer_from_gpt(row,prompt,level=1)
    query_type = find_what_user_expects(row,user_input,level=2).strip() 
    debug_attribute("query_type - ",query_type)  
    debug_steps(row,f"Resmed response - {response_from_resmed}",level=7)
    
    if("sorry" in response_from_resmed and query_type!=SYMPTOM_QUERY and query_type!=PRODUCT_QUERY and query_type!=GENERAL_PRODUCT_QUERY):
        bot_response=response_from_resmed
    elif(query_type == GENERAL_PRODUCT_QUERY):
            prod_response=get_products(row,query_type,user_input,bot_response)
            bot_response = response_from_resmed + prod_response
    elif PRODUCT_QUERY==query_type:
            bot_response=get_products(row,query_type,user_input,bot_response)
    elif(SYMPTOM_QUERY==query_type):
        
        db_input_or_bot_response = identify_symptom(user_input)
        debug_attribute("Identify symptom",db_input_or_bot_response)
        found_symptom = db_input_or_bot_response=="Sleep Apnea" or db_input_or_bot_response=="Insomnia" or db_input_or_bot_response=="Snoring"
        if (SYMPTOM_QUERY in query_type):
            if(found_symptom):
                source = ""
                debug_steps(row,f"{SYMPTOM_QUERY},found symptom & suggest products",level=5)
                MSG = f"This appears to be a condition called {db_input_or_bot_response}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor."
                SLEEP_ASSESSMENT_INFO="For more information please visit'\033]8;;https://info.resmed.co.in/free-sleep-assessment\aSleep Assessment\033]8;;\a'"
                pr_cyan(SLEEP_ASSESSMENT_INFO)
                bot_response= f"{MSG}\n{SLEEP_ASSESSMENT_INFO}"
                output = product(row,db_input_or_bot_response,level=6)
                prod_response = show_products(output)
                bot_response += prod_response
            elif(db_input_or_bot_response=="common"):
                debug_steps(row,f"{SYMPTOM_QUERY}, Symptoms are common",level=5)
                bot_response = "Your symptoms are more common to define the exact syndrome. can you please provide more detail:"
    
    if((not bot_response or len(bot_response)<10) and bot_response!=RESPONSE_FOR_INVALID_QUERY):
        bot_response = response_from_resmed

        
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
            row[1] = bot_response
            csvwriter.writerows([row])
    
    # Add the chatbot's response to the conversation history and print it to the console
    if  response_from_resmed!=RESPONSE_FOR_INVALID_QUERY or response_from_resmed!=UNABLE_TO_FIND_PRODUCTS_IN_DB:
        print("Inside if")
        # User asked an invalid query to our system so, let's remove their query from message logs
        message_log+=f"Human:{user_input}\nAI:{bot_response}{SEPARATORS}"

    pr_bot_response(bot_response)
    return bot_response,message_log
