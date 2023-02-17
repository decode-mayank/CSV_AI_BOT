# Imports
import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'

context = ""

print("Bot: Hello! I'm Resmed Chatbot, a virtual assistant designed to help you with any questions or concerns you may have about Resmed products or services. Resmed is a global leader in sleep apnea treatment, and we're committed to improving the quality of life for people who suffer from sleep-disordered breathing.")
while True:
  my_input = input("User: ")
  context = context + my_input
  

# Calculate embedding vector for the input using OpenAI Embeddings endpoint
  def get_embedding(model,text):
      result = openai.Embedding.create(
        model = model,
        input = text
      )
      return result['data'][0]['embedding']

  # Save embedding vector of the input
  input_embedding_vector = get_embedding(my_model, my_input)

  # Calculate similarity between the input and "facts" from companies_embeddings.csv file which we created before
  df = pd.read_csv('resmed_embeddings.csv')
  df['embedding'] = df['embedding'].apply(eval).apply(np.array)
  df['similarity'] = df['embedding'].apply(lambda x: cosine_similarity(x, input_embedding_vector))

  print(df["similarity"])
  # Find the highest similarity value in the dataframe column 'similarity'
  highest_similarity = df['similarity'].max()

  # If the highest similarity value is equal or higher than 0.9 then print the 'completion' with the highest similarity
  if highest_similarity >= 0.8:
      fact_with_highest_similarity = df.loc[df['similarity'] == highest_similarity, 'completion']
      print(fact_with_highest_similarity.iloc[0])
      
  # Else pass input to the OpenAI Completions endpoint
  else:
    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = my_input,
        max_tokens = 100,
        temperature = 0
      )
    content = response['choices'][0]['text'].replace('\n', '')
    print(content)
