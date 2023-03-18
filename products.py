# imports
import os

import openai
import psycopg2
import sqlparse
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
EMBEDDING_MODEL = "text-embedding-ada-002"

DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND= "Please rephrase your query"

def generate_prompt(text,instruction):
    return f"Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), product_url (character varying), money_back (BOOLEAN), rating (FLOAT), total_reviews (INTEGER). Give a Select query for product, product_url and price, where the category matches to the input question. Format the query in the correct format.{instruction}. Where category can be Sleep Apnea, Snoring or Insomnia, any other Keyword attached with these words can be truncated.{text}"

def execute_query(conn,query):
    sqlparse.format(query, reindent=True, keyword_case='upper')
    debug(query)
    cur = conn.cursor()
    if(query):
        cur.execute(query)
        return cur.fetchall()
    else:
        return DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND

def debug(msg):
    verbose=os.getenv('VERBOSE')
    if verbose=="True":
        print(msg)  

conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

def product(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the rating in Descending order and list top 3 items"),
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
    output = execute_query(conn,query)
    return(output)

def other_products(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the rating in Ascending order and list top 3 items"),
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
    output = execute_query(conn,query)
    return(output)


def cheap_products(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Use Order_by command to order the price in Ascending order and list top 1 items"),
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
    output = execute_query(conn,query)
    return(output)


def general_product(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(text,"Suggest any 2 product as per user Query"),
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
    output = execute_query(conn,query)
    return(output)