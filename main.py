# Imports
from chatbot import resmed_chatbot
from colors import pr_bot_response,pr_red
from constants import MESSAGE_LOG,SYSTEM_PROMPT,SEPARATORS
from debug_utils import debug_attribute
from utils import add_seperators

if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Bot output - Cyan(Normal)
    """
 
    pr_bot_response("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
    
    # message_log = MESSAGE_LOG.copy()
    
    message_log = SYSTEM_PROMPT


    while True:
        input_text = input("User: ").strip()
        if len(input_text) > 100:
            response = ("Please type a message that is less than 100 characters.")
            pr_red(response)
        else:
            # Send the conversation history to the chatbot and get its response
            # Only pass last 3 messages to chat completion API
            
            debug_attribute("Current Message_log Length",len(message_log))
            
            '''
            msg
            ***
            msg
            ***
            msg
            ***
            msg
            '''
            # Store only last 2 conversation and first conversation
            if message_log.find(SEPARATORS) >= 3:
                messages = message_log.split(SEPARATORS)
                last_two_messages = messages[-2:]
                message_log = messages[0] + SEPARATORS + last_two_messages[0] + SEPARATORS+ last_two_messages[1]
                # debug_attribute("Message_log - Length - If",len(message_log))
                # debug_attribute("Message_log ",MESSAGE_LOG)
                # debug_attribute("Message_log Slice",message_log[-2:])
                # message_log = MESSAGE_LOG + message_log[-2:]
                # debug_attribute("Message_log Slice",message_log)
                # debug_attribute("Message_log length after slice",len(message_log))
                
            # debug_attribute("Message_log - Length",len(message_log))
            message_log = add_seperators(message_log)
            
            
            response,message_log = resmed_chatbot(input_text,message_log)
            print("->>>>>>>",response,message_log)

