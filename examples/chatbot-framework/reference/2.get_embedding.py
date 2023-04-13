import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(model: str, text: str) -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result['data'][0]['embedding']


print(get_embedding('text-embedding-ada-002', 'This is a test'))
