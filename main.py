import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import gradio as gr

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'

inputs, outputs = [], []

def get_embedding(model, text):
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']


# Save embedding vector of the input
def resmed_chatbot(input_text, inputs):
    input_embedding_vector = get_embedding(my_model, input_text)

    # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
    df = pd.read_csv('resmed_embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))

    # Find the highest similarity value in the dataframe column 'similarity'
    highest_similarity = df['similarity'].max()

    # If the highest similarity value is equal or higher than 0.8 then print the 'completion' with the highest similarity
    if highest_similarity >= 0.8:
        fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
        fact = fact_with_highest_similarity.iloc[0]
        print(fact)
        outputs.append(fact)
        
    # Else pass input to the OpenAI Completions endpoint
    else:
        prompt = input_text
        if len(inputs) > 0:
            last_input = inputs[-1]
            last_output = outputs[-1]
            prompt = f"{input_text} (based on my previous question: {last_input}, and your previous answer: {last_output})"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0,
        )
        content = response['choices'][0]['text'].replace('\n', '')
        print(content)

while True:
    input_text = input("user:")
    inputs.append(input_text)
    resmed_chatbot(input_text, inputs)


