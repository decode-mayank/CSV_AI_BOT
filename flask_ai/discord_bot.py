import aiohttp
import os
import json
from datetime import datetime, timezone

import discord
import requests

from resources.framework.app.constants import SYSTEM_PROMPT

# Reference - https://www.pragnakalp.com/create-discord-bot-using-python-tutorial-with-examples/

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

message_log = SYSTEM_PROMPT


BASE_URL = f'http://localhost:{os.getenv("FLASK_PORT")}'

# Don't reply in thread

EYES = "👀"
THUMBS_UP = "👍"
THUMBS_DOWN = "👎"
VALID_REACTION = f"Valid reaction are {THUMBS_UP} or {THUMBS_DOWN}"
REPLY_MESSAGE = "Not handling reply message for now"
CLEAR_COMMAND = "/clear"


def call_api(url, data):
    return requests.post(url, json=data)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    async for older_messages in channel.history(limit=1, oldest_first=True):
        first_message = older_messages
        break
    first_message_timestamp = first_message.created_at.replace(
        tzinfo=timezone.utc).timestamp()
    time_stamp = datetime.utcfromtimestamp(
        first_message_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    if "Health-Check-Bot" in message.author.name and message.content == "ping":
        # Health check condition
        await message.channel.send('online')
        return

    if message.content == CLEAR_COMMAND:
        print("User requested to clear channel history")
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

        async for msg in channel.history(limit=num_messages):
            if msg.content != CLEAR_COMMAND or (VALID_REACTION not in msg.content and REPLY_MESSAGE not in msg.content):
                author = msg.author.name
                if "Bot" in author:
                    messages.append(f" Bot: {msg.content}")
                elif len(messages) > 0:
                    messages[-1] = f"Human: {msg.content}" + messages[-1]
                else:
                    print("Got message which sent recently. So, skipping it")

        # Reverse the conversation, so that latest will be shown first
        messages = messages[::-1]
        # Insert System prompt at 0 th index
        messages.insert(0, SYSTEM_PROMPT)

        # Replace with the actual URL of the API endpoint
        url = f"{BASE_URL}/api/chat/"

        data = {
            "user_input": message.content,
            "time_stamp": time_stamp,
            "message_log": messages,
            "discord_id": message.id,
            "html_response": False,
        }

        raw_response = requests.post(url, json=data)
        json_response = json.loads(raw_response.text)

        await message.reply(json_response["response"])


@client.event
async def on_reaction_add(reaction, user):
    message_object = reaction.message
    parent_id = message_object.reference.message_id if message_object.reference else None

    if parent_id:
        url = f"{BASE_URL}/api/feedback/"
        data = {
            "id": None,
            "discord": parent_id
        }
        if reaction.emoji == THUMBS_UP:
            # Replace with the actual URL of the API endpoint
            data["feedback"] = True
            call_api(url, data)
            print("Updated feedback in DB")
            # await reaction.message.reply(f'Hey {user}! you reacted {reaction.emoji} for the message {message}')
        elif reaction.emoji == THUMBS_DOWN:
            data["feedback"] = False
            call_api(url, data)
            # await reaction.message.reply(f'Hey {user}! you reacted {reaction.emoji} for the message {message}')
            print("Updated feedback in DB")
        else:
            await reaction.message.reply(f'Hey {user}! you reacted with {reaction.emoji} - {VALID_REACTION}')

if __name__ == '__main__':
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            client.run(os.getenv("DISCORD_TOKEN"))
        else:
            raise Exception(
                f"Got response status code as {response.status_code}! Please check")
    except aiohttp.ClientConnectorError as e:
        print("Error connecting to Discord server: ", e)
        print("*"*15)
        print("You might be not connected to internet! - Please connect and try again")
    except requests.exceptions.ConnectionError:
        print("Flask server is not running in localhost. Please run this command inside flask_ai directory - flask run command")
