# Imports
from chatbot import resmed_chatbot
from colors import pr_bot_response,pr_red
from constants import MESSAGE_LOG


if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Bot output - Cyan(Normal)
    """
 
    pr_bot_response("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
    
    message_log = MESSAGE_LOG


    while True:
        input_text = input("User: ")
        if len(input_text) > 100:
            response = ("Please type a message that is less than 100 characters.")
            pr_red(response)
        else:
            # Send the conversation history to the chatbot and get its response
            # Only pass last 5 messages to chat completion API
            '''
            1 -> passed -> system -> 1
            2 -> passed -> system, user_input,assistant -> 3
            3 -> passed -> system, user_input,assistant,user_input, assistant -> 5
            Formula: 1+(n-1)*2
            5 -> passed -> system - 1+4*2 = 9 items in message log
            6 -> passed -> system - 1+5*2 = 11 items in message log
            7-> passed -> system - 1+6*2 = 13 items in message log -> 1
            '''
            if len(message_log) > 10:
                message_log = MESSAGE_LOG + message_log[-10:]

            response,message_log = resmed_chatbot(input_text,message_log)

