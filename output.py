import openai
import os
from dotenv import load_dotenv
import gradio as gr
from main import resmed_chatbot, get_embedding, get_db_connection
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'
inputs, outputs = [], []

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = resmed_chatbot(input, history)
    history.append((input, output))
    return history, history 


block = gr.Blocks()
with block:
    gr.Markdown("""<h1><center>Resmed Chatbot</center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Text Here")
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])


block.launch(debug=True)









