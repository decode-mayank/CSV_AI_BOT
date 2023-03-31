import os
import re

import psycopg2  

from constants import SEPARATORS

# Get db connections
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database=os.getenv('DB'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))
    cur = conn.cursor()
    return conn, cur



def add_seperators(message):
    message+=SEPARATORS
    return message

def extract_data(pattern,message):
    results = re.search(pattern, message)
    return results.group(1) if results else ""

def get_props_from_message(message):
    response = message.split("Intent")[0]
    intent,entity,product_suggestion="","",""
    # Extracting the Intent
    intent = extract_data(r'Intent: (.*), Entity', message)
    # Extracting the Entity
    entity = extract_data(r'Entity:\s*(.*),', message)
    # Extracting the Product Suggestion
    product_suggestion = extract_data(r'Product Suggestion:\s*(.*)', message)
    
    return response,intent,entity,product_suggestion