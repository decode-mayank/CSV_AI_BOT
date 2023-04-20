import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from resources.framework.chatbot import get_chat_response
from resources.framework.app.constants import SYSTEM_PROMPT
from resources.framework.utils import update_feedback
import glob
import csv

blp = Blueprint("Products", "products", description="Operations on products")


@blp.route("/api/chat/")
class Product(MethodView):

    def post(self):
        try:
            user_req = request.json

            # check that the required user_input parameter is present in the JSON data
            if 'user_input' not in user_req:
                return {'error': 'user_input parameter is required'}, 400

            # extract the user_input parameter from the JSON data
            user_input = user_req['user_input']

            # extract the optional message_log parameter from the JSON data, if present
            message_log = user_req['message_log']
            if not (isinstance(message_log, list)):
                return {'response': 'Message log should be of type list', 'message_log': []}
            elif len(message_log) == 0:
                message_log = [SYSTEM_PROMPT]
            response, message_log, row_id = get_chat_response(
                user_input, message_log)
            return {'status':True, 'id': row_id, 'response': response, 'message_log': message_log}, 200
        except:
            return {'status':False, 'error': 'invalid request'}, 400


@blp.route("/api/feedback/")
class Feedback(MethodView):

    def post(self):
        data = request.json
        if 'id' not in data or 'feedback' not in data:
            return {'status':False, 'error': 'id or feedback parameter is missing'}, 400

        update_feedback(data['id'], data['feedback'])

        return {'status':True, 'success': True}


@blp.route("/api/hc/")
class HealthCheck(MethodView):

    def get(self):
        return {"status": True}

@blp.route("/api/import/")
class ImportProductCSV(MethodView):

    def get(self):
        for filepath in glob.glob("**.csv"):
            if filepath == 'products.csv':
                with open(filepath, encoding='utf-8-sig') as csv_file:
                    decoded_file = csv_file.read().splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        try:
                            product = Product(category=row['category'], sku=row['sku'], product=row['product'], description=row['description'],
                                                          price=row['price'], breadcrumb=row['breadcrumb'], product_url=row['product_url'], money_back=row['money_back'],
                                                          rating=row['rating'], total_reviews=row['total_reviews'], tags=row['tags'])
                            db.session.add(product)
                            db.session.commit()
                        except:
                            return {"status": False, "message": "Issue while adding Products"}
        return {'status': True, 'message': 'Products successfully added into DB'}, 200
