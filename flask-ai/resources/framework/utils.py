import os
import csv
import psycopg2

from .constants import SEPARATORS
from .debug_utils import debug
from models.chatbot import ChatbotData
from db import db

VERBOSE = os.getenv('VERBOSE')
DEBUG_CSV = os.getenv("DEBUG_CSV")

# Get db connections


def get_db_connection():
    conn = psycopg2.connect(host=os.getenv("DATABASE_HOST"),
                            database=os.getenv('DATABASE_NAME'),
                            user=os.getenv('DATABASE_USER'),
                            password=os.getenv('DATABASE_PASSWORD'))
    cur = conn.cursor()
    return conn, cur


def add_seperators(message):
    message += SEPARATORS
    return message


def get_last_n_message_log(message_log, n):
    '''
        system
        msg
        msg
    '''
    if len(message_log) <= n+1:
        return message_log
    else:
        return [message_log[0]] + message_log[-n:]


def replace_quotes(datas):
    # Bot response may include single quotes when we pass that with conn.execute will return syntax error
    # So, let's replace single quotes with double quotes
    # Reference: https://stackoverflow.com/questions/12316953/insert-text-with-single-quotes-in-postgresql
    record = []
    for data in datas:
        if isinstance(data, str):
            record.append(data.replace("'", "''"))
        else:
            record.append(data)
    return record


def write_to_db(db_status, record):
    row_id = ""
    if db_status:
        [user_input, bot_response, prompt, raw_gpt_response, level1, level2, level3,
            level4, response_accepted, response_time, discord_id, cost, time_stamp] = record

        my_model = ChatbotData(user_input=user_input, bot_response=bot_response, initial_prompt=prompt, initial_response=raw_gpt_response, level1=level1, level2=level2,
                               level3=level3, level4=level4, response_accepted=response_accepted, response_time=response_time, discord_id=discord_id, cost=cost, time_stamp=time_stamp)
        db.session.add(my_model)
        db.session.commit()
        row_id = my_model.id
    else:
        debug("DB insert is disabled")

    return row_id


def update_feedback(id, feedback, discord=False):
    success = False
    # Retrieve the object you want to update
    if discord:
        row = ChatbotData.query.filter(discord_id=id).first()
    else:
        row = ChatbotData.query.get(id)

    if row:
        row.response_accepted = feedback
        db.session.add(row)
        db.session.commit()

    return success


def write_logs_to_csv(mode, fields, row, max_columns, bot_response):
    if VERBOSE == "True":
        debug(f"Writing the logs in {DEBUG_CSV}")
        with open(DEBUG_CSV, mode) as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            if mode == 'w':
                # writing the fields
                csvwriter.writerow(fields)

            row_length = len(row)
            if (row_length != max_columns-1):
                dummy_rows_to_add = max_columns-row_length-2
                row.extend(('-'*dummy_rows_to_add).split('-'))
            # writing the data rows
            row[1] = bot_response
            csvwriter.writerows([row])



def get_or_create(session, model, **kwargs):
    '''
    Creates an object or returns the object if exists
    '''
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        session.merge(instance)
        session.commit()
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance