import os

import openai
from dotenv import load_dotenv
import gradio as gr
import pandas as pd
import numpy as np

from Resmed.file import webpage_chatbot


# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'
inputs, outputs = [], []

message_log = [
        {"role": "system", "content": "Answer the question only related to the topics of sleep,health,mask,sleep disorders from the website https://www.resmed.com.au/knowledge-hub if they ask queries outside of this topics sleep,health,mask,sleep disorders, say That I have been trained to answer only sleep and health related queries"},
        {"role": "assistant", "content": "You are a helpful assistant."}
    ] 

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    message_log.append({"role": "user", "content": input})
    output = webpage_chatbot(input, message_log)
    message_log.append({"role": "assistant", "content": output})
    history.append((input, output))
    return history, history 


block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>Resmed Chatbot</center></h1>""")
    chatbot = gr.Chatbot([("Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing", None)])
    message = gr.Textbox(placeholder="Text Here")
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True)
