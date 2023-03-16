import os
import discord
from main import resmed_chatbot

# Reference - https://www.pragnakalp.com/create-discord-bot-using-python-tutorial-with-examples/

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

message_log = [
    {"role":"system", "content":"You are chatbot of resmed and you can answer to user queries which are related to sleep disorders,mask,health for other queries say I don't know"},
    {"role":"assistant", "content":"You are helpful chatbot of resmed company"}
] 
 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content:
        message_log.append({"role": "user", "content": message.content})
        await message.channel.send(resmed_chatbot(message.content,message_log))


client.run(os.getenv("DISCORD_TOKEN"))