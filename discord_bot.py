import os
import discord
from main import resmed_chatbot

# Reference - https://www.pragnakalp.com/create-discord-bot-using-python-tutorial-with-examples/

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

message_log = [
        {"role": "system", "content": "Answer the question only related to the topics of sleep,health,mask,sleep disorders from the website https://www.resmed.com.au/knowledge-hub if they ask queries outside of this topics sleep,health,mask,sleep disorders, say That I have been trained to answer only sleep and health related queries"}
] 
 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content:
        await message.channel.send(resmed_chatbot(message.content,message_log))


client.run(os.getenv("DISCORD_TOKEN"))