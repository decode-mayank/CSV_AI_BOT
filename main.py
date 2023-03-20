# Imports
from utils import resmed_chatbot
from colors import pr_bot_response,pr_red


INSTRUCTIONS = """
As an AI assistant specialized in sleep-related topics, I am programmed to provide advice and information only on sleep, sleep medicine, mask, snoring, sleep apnea, insomnia, ResMed products, sleep health, and ResMed sleep tests and trackers. Please note that I cannot provide information or advice on topics unrelated to the aforementioned sleep-related topics.
If you have a question that falls outside of these topics, I will not be able to provide a relevant response. In such cases, please respond with the phrase "I'm just a simple AI assistant, I can't help with that."
Please note that while I can provide information and advice, my responses should not be considered a substitute for medical advice from a licensed medical professional. If you have any concerns about your sleep health, please consult a medical professional for further guidance.
"""

if __name__ == '__main__':
    """
    Initial conversation Bot - Cyan(Dark)
    user input - White
    Bot output - Cyan(Normal)
    """
 
    pr_bot_response("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
    
    message_log = [
      {"role":"system","content": INSTRUCTIONS},
    ] 

    while True:
        input_text = input("User: ")
        if len(input_text) > 100:
            response = ("Please type a message that is less than 100 characters.")
            pr_red(response)
        else:
            message_log.append({"role": "user", "content": input_text})
            # Send the conversation history to the chatbot and get its response
            response = resmed_chatbot(input_text,message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
