# imports
import os

import openai
import sqlparse
from dotenv import load_dotenv

from ..debug_utils import debug_steps, debug_attribute
from ..utils import get_db_connection
from ..constants import davinci

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND = "Please rephrase your query"
MODEL, TEMPERATURE, TOKENS = davinci, 0, 200
PRODUCTS_COUNT = 2

conn, cur = get_db_connection()


def call_text_completion(prompt):
    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        temperature=TEMPERATURE,
        max_tokens=TOKENS,
        stop=";"
    )
    response_token_product = response.usage['total_tokens']
    return response, response_token_product


def execute_query(prompt, row, response, level, fn_name):
    results = []
    debug_attribute("DB response", response)
    query = response['choices'][0]['text']
    start = "SELECT"
    start_pos = query.find(start)
    query = query[(start_pos-1):].strip()
    query = sqlparse.format(query, reindent=True, keyword_case='upper')
    if ";" not in query:
        query += ";"
    debug_steps(row, f"{fn_name} - {response}, Additional information: Query-{query},Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},PROMPT-{prompt}", level=level)
    if (query):
        try:
            cur.execute(query)
            results = cur.fetchall()
        except:
            cur.execute("ROLLBACK")
            conn.commit()
        return results
    else:
        return DEFAULT_RESPONSE_WHEN_NO_QUERY_FOUND


def generate_prompt(text, instruction):
    return f"You are a SQL Query generator. Given an input question, respond with syntactically correct PostgreSQL. Be creative but the query must be correct. Only use table called product. The product table has columns: category (character varying), sku (character varying), product (character varying), description (character varying), price (character varying), breadcrumb (character varying), product_url (character varying), money_back (BOOLEAN), rating (FLOAT), total_reviews (INTEGER), tags(character varying).{text} Write an SQL Select query for product, product_url and price that retrieves data from a given table, which should use Where clause to filter data on {text} use only tags column in the WHERE condition if specified by the user query, but can also work without using the tags column if the user query does not require it. Showcase the flexibility and versatility of the query by allowing users to input a parameter to determine whether to use the specified column or not. It should also have only three WHERE conditions that use only the OR operator, while not using category and sku column and AND operator in the WHERE conditions. Showcase how the OR operator can be used effectively to filter data while optimizing query performance, and demonstrate how excluding a column from the WHERE conditions can improve query execution time. Format the query in the correct format. Use case insensitive search for tags column.{instruction}"


def product(row, text, level):
    prompt = generate_prompt(
        text, f"Don't use Where clause at all, Use Order_by command to order the rating OR price in Descending order and list top {PRODUCTS_COUNT} items")
    response, response_token_product = call_text_completion(prompt)
    output = execute_query(prompt, row, response, level, product.__name__)
    return (output, response_token_product)


def other_products(row, text, level):
    prompt = generate_prompt(
        text, f"Use Order_by command to order the rating in Ascending order and list top {PRODUCTS_COUNT} items")
    response, response_token_product = call_text_completion(prompt)
    output = execute_query(prompt, row, response, level,
                           other_products.__name__)
    return (output, response_token_product)


def cheap_products(row, user_input, query_to_db, level):
    if "Product" in query_to_db:
        prompt = generate_prompt(
            user_input, f"Don't use Where clause, Use Order_by command to order the price in Ascending order and list top {PRODUCTS_COUNT} items")
    else:
        prompt = generate_prompt(
            user_input, f"Use Order_by command to order the price in Ascending order and list top {PRODUCTS_COUNT} items")
    response, response_token_product = call_text_completion(prompt)
    output = execute_query(prompt, row, response, level,
                           cheap_products.__name__)
    return (output, response_token_product)


def general_product(row, user_input, query_to_db, level):
    debug_attribute("User input for sql query", query_to_db)
    # Use only tags in condition if there is any product OR category mentioned in user input and
    prompt = generate_prompt(
        query_to_db, f"Use Order_by command to order the rating in Descending order and list top {PRODUCTS_COUNT} items")
    response, response_token_product = call_text_completion(prompt)
    output = execute_query(prompt, row, response, level,
                           general_product.__name__)
    if output == []:
        prompt = generate_prompt(
            user_input, f"Use Order_by command to order the rating in Descending order and list top {PRODUCTS_COUNT} items")
    response, response_token_product = call_text_completion(prompt)
    output = execute_query(prompt, row, response, level,
                           general_product.__name__)
    return (output, response_token_product)
