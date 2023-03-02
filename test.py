# Imports
from utils import get_embedding,resmed_chatbot, get_moderation
import openai
import os
from colorama import Fore, Back, Style

probability = 0

inputs, outputs = [], []


if __name__ == '__main__':
    print(
        Fore.CYAN + Style.BRIGHT + f"Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing." + Style.NORMAL)
    while True:
        input_text = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
        inputs.append(input_text)
        errors = get_moderation(input_text)
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
        resmed_chatbot(input_text, inputs)