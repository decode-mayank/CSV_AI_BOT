# Imports
from utils import resmed_chatbot
from colorama import Fore, Style

if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Highest probability - Magenta
    Bot output - Cyan(Normal)
    Violent Answer - Red
    Other category - Green
    """
 
    print(
        Fore.CYAN + Style.BRIGHT + f"Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing." + Style.NORMAL)
    message_log = [
        {"role": "system", "content": "Answer the question only related to the topics of sleep,health,mask from the website https://www.resmed.com.au/knowledge-hub and if you're unsure of the answer, say That I have been trained to answer only sleep and health related queries"}
    ] 

    first_request = True

    while True:
        if first_request:
            input_text = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
            message_log.append({"role": "user", "content": input_text})

            # Add a message from the chatbot to the conversation history
            message_log.append({"role": "assistant", "content": "You are a helpful assistant."})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(input_text,message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

            first_request = False

        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            input_text = input(Fore.GREEN + Style.BRIGHT + "User: "+ Style.RESET_ALL)

            # If the user types "quit", end the loop and print a goodbye message
            if input_text.lower() == "quit":
                print("Goodbye!")
                break

            message_log.append({"role": "user", "content": input_text})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(input_text,message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

