import os
import discord
from chatbot import chatbot
from app.constants import SYSTEM_PROMPT
from constants import SEPARATORS
from utils import add_seperators, update_feedback
from discord.ext import commands

# Reference - https://www.pragnakalp.com/create-discord-bot-using-python-tutorial-with-examples/

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

message_log = SYSTEM_PROMPT

# Don't reply in thread

EYES = "👀"
THUMBS_UP = "👍"
THUMBS_DOWN = "👎"
VALID_REACTION = f"Valid reaction are {THUMBS_UP} or {THUMBS_DOWN}"
REPLY_MESSAGE = "Not handling reply message for now"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def get_last_n_message_log(message_log, n):
    '''
        system
        ***
        msg
        ***
        msg
        ***
        msg
    '''
    # if we need to get last two messages then we will have 3 *** seperators
    if message_log.find(SEPARATORS) >= n+1:
        messages = message_log.split(SEPARATORS)
        last_n_messages = messages[-n:]

        message_log = messages[0] + SEPARATORS
        for message in last_n_messages:
            message_log += f"{message}{SEPARATORS}"
    else:
        message_log = add_seperators(message_log)
    return message_log


@client.event
async def on_message(message):
    if message.author == client.user:       
        return
    
    if "Health-Check-Bot" in message.author.name and message.content == "ping":
        # Health check condition
        await message.channel.send('online')
        return
    
    if message.content=="/clear":
        channel = message.channel
        if isinstance(channel, discord.TextChannel):
            message_ids = []
            async for message in channel.history(limit=None):
                message_ids.append(message)

            await channel.delete_messages(message_ids)
        else:
            await channel.send("I can't delete messages in a DM channel.")
        
        return
    
    if message.reference is not None:
        await message.reply(REPLY_MESSAGE)
    elif message.content:
        # Reference: https://www.youtube.com/watch?v=XL6ABuJ0XO0
        await message.add_reaction(EYES)

        num_messages = 10
        channel = message.channel
        messages = []

        message_log = add_seperators(SYSTEM_PROMPT)

        async for msg in channel.history(limit=num_messages):
            if VALID_REACTION not in msg.content and REPLY_MESSAGE not in msg.content:
                author = msg.author.name
                if "Bot" in author:
                    messages.append(f" Bot: {msg.content}")
                elif len(messages) > 0:
                    messages[-1] = f"Human: {msg.content}" + messages[-1]
                else:
                    print("Got message which sent recently. So, skipping it")

        # Store only last 2 conversation and prompt conversation
        messages = messages[::-1]
        message_log = message_log + SEPARATORS.join(messages)
        message_log = get_last_n_message_log(message_log, 2)
        response, _ = chatbot(message.content, message_log, message.id)
        await message.reply(response)


@client.event
async def on_reaction_add(reaction, user):
    message_object = reaction.message
    parent_id = message_object.reference.message_id if message_object.reference else None

    if parent_id:
        if reaction.emoji == THUMBS_UP:
            update_feedback(parent_id, True)
            # await reaction.message.reply(f'Hey {user}! you reacted {reaction.emoji} for the message {message}')
        elif reaction.emoji == THUMBS_DOWN:
            # await reaction.message.reply(f'Hey {user}! you reacted {reaction.emoji} for the message {message}')
            update_feedback(parent_id, False)
        else:
            await reaction.message.reply(f'Hey {user}! you reacted with {reaction.emoji} - {VALID_REACTION}')

client.run(os.getenv("DISCORD_TOKEN"))
