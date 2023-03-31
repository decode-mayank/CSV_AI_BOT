# imports
import os

import openai
import sqlparse
from dotenv import load_dotenv

from debug_utils import debug_steps,debug_attribute
from utils import get_db_connection
from constants import davinci

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND= "Please rephrase your query"
MODEL,TEMPERATURE,TOKENS = davinci,0,100

conn,cur = get_db_connection()

def call_text_completion(prompt):
    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,        
        temperature=TEMPERATURE,
        max_tokens=TOKENS,
        stop=";"
    )
    return response

def execute_query(prompt,row,response,level,fn_name):
    debug_attribute("DB response",response)
    query = response['choices'][0]['text']
    start = "SELECT"
    start_pos = query.find(start)
    query = query[(start_pos-1):].strip().replace("AND", "OR")
    query = sqlparse.format(query, reindent=True, keyword_case='upper')
    debug_steps(row,f"{fn_name} - {response}, Additional information: Query-{query},Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},PROMPT-{prompt}",level=level)
    if(query):
        try:
            cur.execute(query)
        except:
            pass
        return cur.fetchall()
    else:
        return DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND


def generate_prompt(text,instruction):
    return f"Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), product_url (character varying), money_back (BOOLEAN), rating (FLOAT), total_reviews (INTEGER), tags(character varying). Give a Select query for product, product_url and price, where the tags matches to the input question.{text}. Format the query in the correct format.Use case insensitive search for tags column.{instruction}"

def product(row,text,level):
    prompt=generate_prompt(text,"Use Order_by command to order the rating in Descending order and list top 3 items")
    response = call_text_completion(prompt)
    output = execute_query(prompt,row,response,level,product.__name__)
    return(output)

def other_products(row,text,level):
    prompt=generate_prompt(text,"Use Order_by command to order the rating in Ascending order and list top 3 items")
    response = call_text_completion(prompt)
    output = execute_query(prompt,row,response,level,other_products.__name__)
    return(output)


def cheap_products(row,text,level):
    prompt=generate_prompt(text,"Use Order_by command to order the price in Ascending order and list top 1 items")
    response = call_text_completion(prompt)
    output = execute_query(prompt,row,response,level,cheap_products.__name__)
    return(output)


def general_product(row,text,user_input,level):  
    if text=="" or "Product" in text:
        prompt=generate_prompt(user_input,"Suggest any 2 product as per user Query. Write an SQL query that retrieves data from table based on a specified condition. Use only tags in condition if there is any product OR category mentioned in user input and if Multiple conditions go only with OR command. Use atmost three conditions in where clause")
    else:
        prompt=generate_prompt(text,"Suggest any 2 product as per user Query. Write an SQL query that retrieves data from table based on a specified condition. Use only tags in condition if there is any product OR category mentioned in user input and if Multiple conditions go only with OR command. Use atmost three conditions in where clause")
    response = call_text_completion(prompt)
    output = execute_query(prompt,row,response,level,general_product.__name__)
    return(output)
