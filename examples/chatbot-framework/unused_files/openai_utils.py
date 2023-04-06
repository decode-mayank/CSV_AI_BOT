import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from constants import ada
from debug_utils import debug,debug_steps

# Calculate embedding vector for the input using OpenAI Embeddings endpoint
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(text):
    result = openai.Embedding.create(
        model=ada,
        input=text
    )
    return result['data'][0]['embedding']


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


# Zero shot learning
def call_chat_completion_api(row,message_log,level):
    debug("Let's ask Chat completion API to answer user query") 
    PROMPT,MODEL,TOKENS,TEMPERATURE = message_log,turbo,150,0
    # bot_response=""
    response = openai.ChatCompletion.create(
            model=MODEL,
            messages = PROMPT,
            max_tokens=TOKENS,
            temperature=TEMPERATURE
            # stream=True
        )
    

    # TODO: Once everything works fine then switch back to stream
    # pr_bot_response("",end="")
    # for chunk in response:
    #     if "content" in chunk.choices[0].delta.keys():
    #         bot_response+=chunk.choices[0].delta.content
    #         pr_cyan(f"{chunk.choices[0].delta.content}",end="")
    # print()
    
    debug_steps(row,f'{level} - {call_chat_completion_api.__name__} - {response}, Additional information: Model-{MODEL}, Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE}, PROMPT-{PROMPT}"',level)
    response_text = response.choices[0].message.content.strip()
    response_tokens = response.usage['total_tokens']
    return response_text, response_tokens