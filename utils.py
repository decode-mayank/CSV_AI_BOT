import os
import csv 
import psycopg2  

from constants import SEPARATORS
from debug_utils import debug

VERBOSE = os.getenv('VERBOSE')

DEBUG_CSV = os.getenv("DEBUG_CSV")

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


def get_last_n_message_log(message_log,n):
    '''
        system
        ***
        msg
        ***
        msg
        ***
        msg
    '''
    # if we need to get last two messages then we will have 3 *** seperators
    if message_log.find(SEPARATORS) >= n+1:
        messages = message_log.split(SEPARATORS)
        last_n_messages = messages[-n:]
        
        message_log = messages[0] + SEPARATORS 
        for message in last_n_messages:
            message_log += f"{message}{SEPARATORS}"
    else:
        message_log = add_seperators(message_log)
    return message_log

def write_to_db(db,user_input,bot_response,probability,response_accepted,response_time,time_stamp,source):
    if db:
        query = f"INSERT INTO chatbot_datas (prompt,completion,probability,response_accepted,response_time,time_stamp,source) VALUES('{user_input}','{bot_response}','{probability}','{response_accepted}',{response_time},'{time_stamp}','{source}');"
        debug(f"Query to execute - {query}")
        conn,cur = get_db_connection()
        cur.execute(query)
        conn.commit()
        debug("Data added successfully")
    else:
        debug("DB insert is disabled")
     
def write_logs_to_csv(mode,fields,row,max_columns,bot_response):
    if VERBOSE=="True":
        debug(f"Writing the logs in {DEBUG_CSV}")
        with open(DEBUG_CSV, mode) as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            if mode=='w':
                # writing the fields 
                csvwriter.writerow(fields) 
                
            row_length = len(row)
            if(row_length!=max_columns-1):
                dummy_rows_to_add = max_columns-row_length-2
                row.extend(('-'*dummy_rows_to_add).split('-'))
            # writing the data rows 
            row[1] = bot_response
            csvwriter.writerows([row])

