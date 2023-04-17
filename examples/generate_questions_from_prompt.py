import os
import openai
from dotenv import load_dotenv
import csv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot(num_of_sets):
    response_list = []
    for _ in range(num_of_sets):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="As a question provider, your task is to generate questions that users may ask ResMed chatbot from their perspective. These questions do not necessarily have to be professional and can be about random or tricky topics.Each time don't repeat the same questions. Please focus on sleep apnea, snoring, and insomnia and encourage users to share their symptoms. For example, a user may ask: 'I often feel very tired, Why do I wake up feeling exhausted, even if I've slept for a full eight hours?",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        
        response_text = response.choices[0].text.strip()
        response_list.append(response_text)
        print(response_text)
    
    with open('responses.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell()==0:
            writer.writerow(['Response'])
        for response in response_list:
            writer.writerow([response])
            writer.writerow(["*"*15])
            
chatbot(5)