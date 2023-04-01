# Imports
from chatbot import resmed_chatbot
from colors import pr_bot_response,pr_red
from constants import SYSTEM_PROMPT,SEPARATORS
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
 
    pr_bot_response("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
    
    
    message_log = SYSTEM_PROMPT


    while True:
        input_text = input("User: ").strip()
        if len(input_text) > 100:
            response = ("Please type a message that is less than 100 characters.")
            pr_red(response)
        else:            
            debug_attribute("Current Message_log Length",len(message_log))
              
            if message_log.find(SEPARATORS) >= 4:
                messages = message_log.split(SEPARATORS)
                last_two_messages = messages[-3:]
                message_log = messages[0] + SEPARATORS + last_two_messages[0] + SEPARATORS+ last_two_messages[1]+SEPARATORS+ last_two_messages[2]
                
                
            # Store only last 2 conversation and prompt conversation
            message_log = get_last_n_message_log(message_log,2)
            
            response,message_log = resmed_chatbot(input_text,message_log)
            print("->>>>>>>",response)
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>",message_log)

