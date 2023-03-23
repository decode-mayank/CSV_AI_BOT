# imports
import os

import openai
import psycopg2
import sqlparse
from dotenv import load_dotenv
from debug_utils import debug_steps

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
EMBEDDING_MODEL = "text-embedding-ada-002"

DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND= "Please rephrase your query"

def generate_prompt(text,instruction):
    return f"Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), product_url (character varying), money_back (BOOLEAN), rating (FLOAT), total_reviews (INTEGER), tags(character varying). Give a Select query for product, product_url and price, where the tags matches to the input question.{text}. Format the query in the correct format.Use case insensitive search for tags column.{instruction}"

def execute_query(conn,row,response,fn_name):
    query = response['choices'][0]['text']
    start = "SELECT"
    end = ";"
    start_pos = query.find(start)
    end_pos = query.find(end)
    query = query[(start_pos-1):(end_pos+1)].strip()
    sqlparse.format(query, reindent=True, keyword_case='upper')
    debug_steps(row,f"DB Query from {fn_name}",query)
    cur = conn.cursor()
    if(query):
        cur.execute(query)
        return cur.fetchall()
    else:
        return DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND


conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

def product(row,text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the rating in Descending order and list top 3 items"),
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    output = execute_query(conn,row,response,product.__name__)
    return(output)

def other_products(row,text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the rating in Ascending order and list top 3 items"),
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    output = execute_query(conn,row,response,other_products.__name__)
    return(output)


def cheap_products(row,text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the price in Ascending order and list top 1 items"),
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    output = execute_query(conn,row,response,cheap_products.__name__)
    return(output)


def general_product(row,text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), product_url (character varying), money_back (BOOLEAN), rating (FLOAT), total_reviews (INTEGER), tags (character varying). Understand the user input correctly and create a SQL query. Give a Select query for product, product_url and price.{text}. Format the query in the correct format. Suggest any 2 product as per user Query. Write an SQL query that retrieves data from table based on a specified condition. The query should return specific columns and have proper formatting and syntax. Use tags in condition if there is any product or category mentioned in user input and if Multiple conditions go with OR command. Use case insensitive search for tags column",        
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    query = response['choices'][0]['text']
    start = "SELECT"
    end = ";"
    start_pos = query.find(start)
    end_pos = query.find(end)
    query = query[(start_pos-1):(end_pos+1)].strip()

    output = execute_query(conn,row,response,general_product.__name__)
    return(output)