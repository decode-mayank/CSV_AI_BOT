# Imports
from Resmed.file import SYSTEM_PROMPT, initial_conversation
from colors import pr_bot_response,pr_red
from constants import SEPARATORS
from chatbot import webpage_chatbot
from debug_utils import debug_attribute
from utils import add_seperators


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

if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Bot output - Cyan(Normal)
    """
    
    pr_bot_response(initial_conversation)
    
    
    message_log = SYSTEM_PROMPT


    while True:

        input_text = input("User: ").strip()
        if len(input_text) > 300:
            response = ("Please type a message that is less than 300 characters.")
            pr_red(response)
        else:                       
            # Store only last 2 conversation and prompt conversation
            message_log = get_last_n_message_log(message_log,2)
            
            response,message_log = webpage_chatbot(input_text,message_log)
            print("->>>>>>>",response)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>",message_log)

