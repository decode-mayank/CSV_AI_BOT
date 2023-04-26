# Imports
from app.constants import SYSTEM_PROMPT, INITIAL_MESSAGE
from colors import pr_bot_response
from chatbot import get_chat_response

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':

    pr_bot_response(INITIAL_MESSAGE)

    message_log = [SYSTEM_PROMPT]

    while True:
        user_input = input("User: ").strip()
        response, message_log = get_chat_response(user_input, message_log)
        print("-"*16, "Response", response)
        print("*"*16, "Message log", message_log, len(message_log))
