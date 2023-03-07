# imports
import openai
import os
import psycopg2
from colorama import Fore, Back, Style
from dotenv import load_dotenv
import sqlparse


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# constants
EMBEDDING_MODEL = "text-embedding-ada-002"


conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

def product(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), and product_url (character varying). Give a Select query for product and product_url, where the category matches to the input question. Format the query in the correct format. Use Order_by command to order the rating in Descending order and list top 2 items." + text,
        temperature=0.3,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    query = response['choices'][0]['text'].replace('\n', '')
    sqlparse.format(query, reindent=True, use_space_around_operators=True)
    # print(sqlparse.format(query, reindent=True, use_space_around_operators=True))
    cur = conn.cursor()
    cur.execute(query)
    print(cur.fetchall())
