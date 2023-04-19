import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Products", "products", description="Operations on products")

# @blp.route("/api/")
# class Product(MethodView):