import csv
import glob
import json
import os
import re
import requests
import time
from datetime import datetime

from flask import request, make_response, Response
from flask_smorest import Blueprint
from flask.views import MethodView
import openai

from db import db
from models.chatbot import Product
from resources.framework.chatbot import get_chat_response
from resources.framework.app.constants import SYSTEM_PROMPT
from resources.framework.utils import update_feedback, get_or_create
import openai
from resources.framework.stream import chatbot_stream


blp = Blueprint("ChatbotData", "chatbot_data",
                description="Provide answer of user questions by chatbot")
pblp = Blueprint("Product", "products",
                 description="Insert products from csv to db")
dhcblp = Blueprint("Discord Health Check", "discord health check",
                   description="Discord Health Check API")

CHANNEL_ID = os.getenv('HEALTH_CHECK_CHANNEL_ID')
URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"


@blp.route("/api/chat/")
class UserChatBot(MethodView):

    def post(self):
        try:
            user_req = request.json

            # check that the required user_input parameter is present in the JSON data
            if 'user_input' not in user_req:
                return {'status': False, 'response': 'user_input parameter is required'}, 400

            # extract the user_input parameter from the JSON data
            user_input = user_req['user_input']

            # extract the optional message_log parameter from the JSON data, if present
            message_log = user_req.get('message_log', [SYSTEM_PROMPT])
            html_response = user_req.get('html_response', True)
            time_stamp = user_req.get(
                'time_stamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            discord_id = user_req.get('discord_id', None)

            if not (isinstance(message_log, list)):
                return {"status": False,'response': 'Message log should be of type list', 'message_log': []}, 400

            pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

            if not (pattern.match(time_stamp)):
                return {"status": False,'response': 'time_stamp is not in expected format - Example: 2023-04-27 08:16:07'}, 400

            response, new_message_log, row_id = get_chat_response(
                user_input, message_log, time_stamp, html_response, discord_id)
            return {'status': True, 'id': row_id, 'response': response, 'message_log': new_message_log}, 200
        except openai.error.RateLimitError:
            return {'status': False, "response": "OpenAI API Rate Limit Error"}, 429
        except:
            return {'status': False, "response": "We are unable to serve your request at this time"}, 500


@blp.route("/api/feedback/")
class Feedback(MethodView):

    def post(self):
        data = request.json
        if ('id' not in data or 'discord' not in data) and 'feedback' not in data:
            return {'status': False, 'error': 'id or feedback parameter is missing'}, 400

        update_feedback(data.get('id', None),
                        data['feedback'], data.get('discord', None))

        return {'status': True, 'success': True}



@pblp.route("/api/import/")
class ImportProductCSV(MethodView):

    def get(self):
        status = False
        PRODUCTS_CSV = "products.csv"
        files = glob.glob(PRODUCTS_CSV)
        if PRODUCTS_CSV in files:
            with open(PRODUCTS_CSV, encoding='utf-8-sig') as csv_file:
                decoded_file = csv_file.read().splitlines()
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    try:
                        get_or_create(db.session, Product, category=row['category'], sku=row['sku'], product=row['product'], description=row['description'],
                                      price=row['price'], breadcrumb=row['breadcrumb'], product_url=row['product_url'], money_back=eval(
                            row['money_back']),
                            rating=row['rating'], total_reviews=row['total_reviews'], tags=row['tags'], type=row['type'])
                        status = True
                    except:
                        return {"status": status, "message": "Issue while adding Products"}, 500
        else:
            return {"status": status, "message": "Issue while adding Products"}, 500
        return {'status': status}, 200


def call_api(url, method, data=None):
    headers = {
        "Authorization": f"Bot {os.getenv('DISCORD_HEALTH_CHECK_TOKEN')}",
        "Content-Type": "application/json"
    }

    if (method == "GET"):
        response = requests.get(url, headers=headers)
    elif (method == "POST"):
        response = requests.post(url, headers=headers, json=data)
    else:
        raise Exception(f"Invalid method - {method}")

    return response


def write_json_response(object):
    # Convert the dictionary to a JSON string
    response_json = json.dumps(object)
    # Write the JSON string to the response body
    return response_json


def default_response(object):
    response = make_response(write_json_response(object))
    response.status_code = 500
    return response


@dhcblp.route('/api/discord-health-check')
def discord_health():
    if CHANNEL_ID:
        send_message_response = call_api(
            URL, "POST", {
                "content": "ping"
            })

        if (send_message_response.status_code == 200):
            time.sleep(5)
            get_message_response = call_api(
                f"{URL}?limit=1", "GET")
            if (get_message_response.status_code == 200):
                content = get_message_response.json()[0]["content"]

                if (content == "online"):
                    # Set the response status code and content type
                    response = make_response(
                        write_json_response({"success": True}))
                    response.status_code = 200
                    return response
                else:
                    return default_response({
                        "success": False, "error": f"Invalid response from get message API - {content}"})
            else:
                return default_response({
                    "success": False, "error": f"Got {get_message_response.status_code} status code from get_message API"})
        else:
            return default_response({
                "success": False, "error": f"Got {send_message_response.status_code} status code from send message API"})
    else:
        response = make_response(
            write_json_response({"success": False, "error": "In env, HEALTH_CHECK_CHANNEL_ID is missing"}))
        response.status_code = 500
        return response


@blp.route("/api/stream/")
class ChatBotStream(MethodView):

    def post(self):
        # try:
        user_req = request.json

        # check that the required user_input parameter is present in the JSON data
        if 'user_input' not in user_req:
            return {'error': 'user_input parameter is required'}, 400

        # extract the user_input parameter from the JSON data
        user_input = user_req['user_input']

        # extract the optional message_log parameter from the JSON data, if present
        message_log = user_req.get('message_log', [SYSTEM_PROMPT])
        html_response = user_req.get('html_response', True)
        time_stamp = user_req.get(
            'time_stamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        discord_id = user_req.get('discord_id', None)

        if not (isinstance(message_log, list)):
            return {'response': 'Message log should be of type list', 'message_log': [], "status": False}, 400

        pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

        if not (pattern.match(time_stamp)):
            return {'response': 'time_stamp is not in expected format - Example: 2023-04-27 08:16:07', "status": False}, 400

        bot_response, message_log, row_id = chatbot_stream(user_input, message_log, time_stamp, html_response, discord_id)
        def generate_response():
            for response_chunk in bot_response.split(' '):
                chunk = response_chunk + ' '
                yield f'data: {{"stream": "{chunk}"}}\n\n'
                time.sleep(0.2)
            yield f'data: {{"message_log": {message_log}, "row_id": "{row_id}"}}\n\n'

        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        return Response(generate_response(), mimetype="text/event-stream", headers=headers)
        # except:
        #     return {'status': False}, 500












