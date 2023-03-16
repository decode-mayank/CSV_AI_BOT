# Imports
from utils import resmed_chatbot

from colors import pr_bot_response,pr_red

if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Bot output - Cyan(Normal)
    """
 
    pr_bot_response("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
    
    message_log = [
        # {"role": "system", "content": "Answer the question only related to the topics of sleep,health,mask,sleep disorders from the website https://www.resmed.com.au/knowledge-hub if they ask queries outside of this topics sleep,health,mask,sleep disorders, say That I have been trained to answer only sleep and health related queries"}
         {"role":"system", "content":"You are chatbot of resmed and you can answer to user queries which are related to sleep disorders,mask,health for other queries say I don't know"},
         {"role":"assistant", "content":"You are helpful chatbot of resmed company"}
    ] 

    first_request = True

    while True:
        if first_request:
            input_text = input("User: ")
            message_log.append({"role": "user", "content": input_text})

            if len(input_text) > 500:
                pr_red("Please type a message that is less than 500 characters.")
                continue

            # Add a message from the chatbot to the conversation history
            message_log.append({"role": "assistant", "content": "You are a helpful assistant."})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(input_text,message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

            first_request = False

        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            input_text = input("User: ")
            # If the user types "quit", end the loop and print a goodbye message
            if input_text.lower() == "quit":
                print("Goodbye!")
                break

            if len(input_text) > 500:
                pr_red("Please type a message that is less than 500 characters.")
                continue

            message_log.append({"role": "user", "content": input_text})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(input_text,message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

