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

def get_props_from_message(message):
    response = message.split("Intent")[0]
    # Extracting the Intent
    intent = re.search(r'Intent: (.*), Entity', message).group(1)
    # Extracting the Entity
    entity = re.search(r'Entity:\s*(.*),', message).group(1)
    # Extracting the Product Suggestion
    product_suggestion = re.search(r'Product Suggestion:\s*(.*)', message).group(1)
    
    return response,intent,entity,product_suggestion