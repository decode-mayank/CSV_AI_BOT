import os
import openai
import gtts
import playsound
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()
start_sequence = "\nBitcotAI:"
restart_sequence = "\n\nPerson:"
session_prompt = "I want you to act as a Customer Service Bot for https://www.bitcot.com/ , You as a chatbot should have full knowledge on https://www.bitcot.com/  website and respond to customers queries from the website. Have end-to-end knowledge on the website.\n\nPerson: Who are You?\n\nBitcotAI: I am BitcotAI, chatbot at Bitcot Technology\n\nPerson: How to contact you?\n\nBitcotAI: You can refer to ContactUs Page in out website or also contact us through support@bitcot.com\n\nPerson: What are the servives you provide?\n\nBitcotAI: Bitcot offers a wide range of services for our clients. Some of our main services include:\n\nWebsite development and design, Mobile app development, E-commerce solutions, Digital marketing and SEO, Custom software development, Cloud solutions and hosting, Maintenance and support, IT consulting"
session = {'chat_log': session_prompt}
AUDIO_FILE = "output.mp3" # This file is used to save the audio of bot response


def ask(prompt, chat_log):
    prompts = f'{chat_log}{restart_sequence}: {prompt}{start_sequence}:'
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompts,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message.strip()


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
        

def chatbot(user_input):
    print(user_input)
    chat_log = session['chat_log']
    bot_response = ask(user_input, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(user_input, bot_response, chat_log)
    print("BitcotAI:", bot_response)
    sound = gtts.gTTS(bot_response, lang="en")
    sound.save(AUDIO_FILE)
    playsound.playsound(AUDIO_FILE)
    
if __name__ == "__main__":
    try:
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Please say something")
                audio = r.listen(source)
                user_input = r.recognize_google(audio)
                
                if user_input=="keyboard" :
                    user_input=input("text here : ")
                    
                chatbot(user_input)
                
                if "bye" in user_input:
                    break
    except sr.UnknownValueError:
        print("Sorry could not recognize your voice")
