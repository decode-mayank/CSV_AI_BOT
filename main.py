# Imports
from app.constants import SYSTEM_PROMPT, INITIAL_MESSAGE
from colors import pr_bot_response,pr_red
from chatbot import chatbot
from utils import get_last_n_message_log

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    
    pr_bot_response(INITIAL_MESSAGE)

    message_log = SYSTEM_PROMPT
    
    while True:
        input_text = input("User: ").strip()
        if len(input_text) > 300:
            response = ("Please type a message that is less than 300 characters.")
            pr_red(response)
        else:                       
            # Store only last 2 conversation and prompt conversation
            message_log = get_last_n_message_log(message_log,2)
            response,message_log = chatbot(input_text,message_log)
        print("-"*16,"Response",response)
        print("*"*16,"Message log",message_log)
