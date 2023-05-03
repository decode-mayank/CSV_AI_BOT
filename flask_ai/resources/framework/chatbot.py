from datetime import datetime
import json
import os
import time

import openai
from dotenv import load_dotenv

from .colors import pr_bot_response, pr_red
from .debug_utils import debug_steps, debug, debug_attribute
from .constants import davinci, HUMAN, BOT, INITIAL_PROMPT, INITIAL_RESPONSE, COST, fields_dict
from .utils import get_db_connection, replace_quotes, write_to_db, write_logs_to_csv, get_last_n_message_log
from .app.utils import chatbot_logic, get_props_from_message
from .app.constants import RESPONSE_FOR_INVALID_QUERY, UNABLE_TO_FIND_PRODUCTS_IN_DB, CHATBOT_NAME

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# constants
DEBUG_CSV = os.getenv("DEBUG_CSV")
VERBOSE = os.getenv('VERBOSE')

conn, cur = get_db_connection()
# constants


def get_answer_from_gpt(row, prompt, level):
    # Multi shot learning
    TOKENS, TEMPERATURE, MODEL, STOP = 200, 0, davinci, [HUMAN, BOT]
    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        temperature=TEMPERATURE,
        max_tokens=TOKENS,
        stop=STOP
    )

    debug_steps(row, f"{level} - {get_answer_from_gpt.__name__} - {json.dumps(response)}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},STOP-{STOP},PROMPT-{prompt}", level)

    response_text = response.choices[0].text.strip()
    response_token = response.usage['total_tokens']
    return response_text, response_token


def get_chat_response(user_input, message_log, time_stamp, html_response, discord_id, db=True):
    updated_message_log, row_id = "", ""
    if len(user_input) > 300:
        response = "Please type a message that is less than 300 characters."
        pr_red(response)
    else:
        response, updated_message_log, row_id = chatbot(
            user_input, message_log, time_stamp, html_response, discord_id, db)
    return response, updated_message_log, row_id


def chatbot(user_input, message_log, time_stamp, html_response, discord_id, db):
    # Store only last 2 conversation and prompt conversation
    message_log = get_last_n_message_log(message_log, 2)
    MODE = 'w'
    fields = ["user_input", "bot_response", "level1", "level2", "level3", "level4",
              INITIAL_PROMPT, INITIAL_RESPONSE, COST]
    MAX_COLUMNS = len(fields)
    row = [""] * MAX_COLUMNS
    row[0] = user_input

    valid_query = True

    if os.path.exists(DEBUG_CSV):
        MODE = 'a'

    prompt = "\n".join(message_log) + f"{HUMAN}{user_input}{BOT}"

    debug_steps(row, f"Prompt - {prompt}", level=INITIAL_PROMPT)

    response_accepted = True
    bot_response = ""

    response_time = 0

    start_time = time.time()

    raw_gpt_response, gpt_tokens = get_answer_from_gpt(row, prompt, level=1)
    debug_attribute("gpt_tokens - ", gpt_tokens)
    debug_steps(
        row, f"webpage response - {raw_gpt_response}", level=INITIAL_RESPONSE)

    query_to_tokens = 0

    response_in_lower_case = raw_gpt_response.lower()
    props = get_props_from_message(raw_gpt_response)

    if ("sorry" in response_in_lower_case or CHATBOT_NAME in response_in_lower_case):
        '''
        We will reach this if query in this order
        i) Suggest me good songs which I can listen before sleep 
        ii) Write a poem for sleep
        '''
        response, *_ = props
        bot_response = response
        valid_query = False
    else:
        bot_response, raw_response, tokens = chatbot_logic(
            props, row, user_input, raw_gpt_response, html_response)
        query_to_tokens = tokens

    debug_attribute("query_to_tokens - ", query_to_tokens)
    response_time = time.time() - start_time

    token_calculation = gpt_tokens + query_to_tokens
    cost_of_davinci = 0.0200
    cost = (token_calculation * cost_of_davinci) / 1000
    debug_steps(row, f"total cost - {cost}", level=COST)

    record = replace_quotes([user_input, bot_response, prompt, raw_gpt_response, row[fields_dict[1]], row[fields_dict[2]],
                            row[fields_dict[3]], row[fields_dict[4]], response_accepted, response_time, discord_id, cost, time_stamp])
    row_id = write_to_db(db, record)

    debug(f"Response time in seconds - {response_time}")

    write_logs_to_csv(MODE, fields, row, MAX_COLUMNS, bot_response)

    # Add the chatbot's response to the conversation history
    if raw_gpt_response not in UNABLE_TO_FIND_PRODUCTS_IN_DB and valid_query and raw_gpt_response not in RESPONSE_FOR_INVALID_QUERY:
        message_log.append(f"{HUMAN}{user_input}\n{BOT}{raw_response}")

    pr_bot_response(bot_response)
    print(f"Total cost - {cost}")
    return bot_response, message_log, row_id
