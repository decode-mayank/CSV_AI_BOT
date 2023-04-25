import csv
import glob

from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView

from db import db
from models.chatbot import Product
from resources.framework.chatbot import get_chat_response
from resources.framework.app.constants import SYSTEM_PROMPT
from resources.framework.utils import update_feedback, get_or_create


blp = Blueprint("ChatbotData", "chatbot_data",
                description="Provide answer of user questions by chatbot")
pblp = Blueprint("Product", "products",
                 description="Insert products from csv to db")


@blp.route("/api/chat/")
class UserChatBot(MethodView):

    def post(self):
        try:
            user_req = request.json

            # check that the required user_input parameter is present in the JSON data
            if 'user_input' not in user_req:
                return {'error': 'user_input parameter is required'}, 400

            # extract the user_input parameter from the JSON data
            user_input = user_req['user_input']

            # extract the optional message_log parameter from the JSON data, if present
            message_log = user_req.get('message_log', [SYSTEM_PROMPT])

            if not (isinstance(message_log, list)):
                return {'response': 'Message log should be of type list', 'message_log': []}

            response, new_message_log, row_id = get_chat_response(
                user_input, message_log)
            return {'status': True, 'id': row_id, 'response': response, 'message_log': new_message_log}, 200
        except:
            return {'status': False, 'error': 'invalid request'}, 400


@blp.route("/api/feedback/")
class Feedback(MethodView):

    def post(self):
        data = request.json
        if 'id' not in data or 'feedback' not in data:
            return {'status': False, 'error': 'id or feedback parameter is missing'}, 400

        update_feedback(data['id'], data['feedback'])

        return {'status': True, 'success': True}


@blp.route("/api/hc/")
class HealthCheck(MethodView):

    def get(self):
        return {"status": True}


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
                                        rating=row['rating'], total_reviews=row['total_reviews'], tags=row['tags'])
                        status=True
                    except:
                        return {"status": status, "message": "Issue while adding Products"}, 500
        else:
            return {"status": status, "message": "Issue while adding Products"}, 500
        return {'status': status}, 200
