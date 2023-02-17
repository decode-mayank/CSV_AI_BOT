# Imports
import openai
from openai.embeddings_utils import cosine_similarity
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# Insert your API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Insert OpenAI text embedding model and input
my_model = 'text-embedding-ada-002'

context = ""


def get_moderation(question):
    """
    Check the question is safe to ask the model
    Parameters:
        question (str): The question to check
    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


while True:
  my_input = input(Fore.GREEN + Style.BRIGHT + "User: " + Style.RESET_ALL)
  context = context + my_input
  errors = get_moderation(my_input)
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
      print(Fore.CYAN + Style.BRIGHT + fact_with_highest_similarity.iloc[0] + Style.NORMAL)
      
  # Else pass input to the OpenAI Completions endpoint
  else:
      response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = my_input,
        max_tokens = 100,
        temperature = 0
      )
      content = response['choices'][0]['text'].replace('\n', '')
      print(Fore.CYAN + Style.BRIGHT + content+ Style.NORMAL)
