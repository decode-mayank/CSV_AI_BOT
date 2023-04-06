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
    entity = extract_data(r'Entity: (.*), Product Suggestion', message)
    # Extracting the Product Suggestion
    product_suggestion = extract_data(r'Product Suggestion: (.*), Price Range', message)
    # Extract price range
    price_range = extract_data(r'Price Range:\s*(.*)', message)
    
    return response,intent,entity,product_suggestion,price_range

# print(get_props_from_message("""Here are some tips to help you get a good night's sleep: 
# 1. Stick to a regular sleep schedule - go to bed and wake up at the same time every day. 
# 2. Avoid caffeine, nicotine, and alcohol before bed. 
# 3. Exercise regularly, but not too close to bedtime. 
# 4. Avoid large meals and beverages late at night. 
# 5. Relax before bed by taking a warm bath or reading a book. 
# 6. Make sure your bedroom is dark, quiet, and comfortable. 
# 7. If you can't sleep, get out of bed and do something relaxing until you feel tired. 
# Intent: Healthy Sleep Tips, Entity: Healthy Sleep Tips, Product Suggestion: Resmed, Price Range: None."""))
