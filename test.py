# Imports
from utils import get_embedding,resmed_chatbot, get_moderation
import openai
import os
from colorama import Fore, Back, Style

probability = 0

inputs, outputs = [], []


if __name__ == '__main__':
    # print(
        # Fore.CYAN + Style.BRIGHT + f"Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing." + Style.NORMAL)
    message_log = [
        {"role": "system", "content": "Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing."}
    ] 

    first_request = True

    while True:
        #breakpoint()
        if first_request:
            user_input = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
            message_log.append({"role": "user", "content": user_input})

            # Add a message from the chatbot to the conversation history
            message_log.append({"role": "assistant", "content": "You are a helpful assistant."})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

            first_request = False

            #inputs.append(input_text)
            errors = get_moderation(user_input)
            if errors:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "Sorry, you're question didn't pass the moderation check:"
                )
                for error in errors:
                    print(error)
                print(Style.RESET_ALL)
                continue
            resmed_chatbot(message_log)
            #resmed_chatbot(input_text, inputs)

        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            user_input = input("User: ")

            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

