from db import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(500))
    sku = db.Column(db.String(500))
    product = db.Column(db.String(500))
    description = db.Column(db.String(5000), nullable=True)
    price = db.Column(db.Float)
    breadcrumb = db.Column(db.String(500), nullable=True)
    product_url = db.Column(db.String(500), nullable=True)
    money_back = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, nullable=True)
    total_reviews = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.String(500), nullable=True)


class ChatbotData(db.Model):
    __tablename__ = 'chatbot_datas'

    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text())
    bot_response = db.Column(db.Text())
    initial_prompt = db.Column(db.Text())
    initial_response = db.Column(db.Text())
    level1 = db.Column(db.Text())
    level2 = db.Column(db.Text())
    level3 = db.Column(db.Text())
    level4 = db.Column(db.Text())
    response_accepted = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.SmallInteger)
    discord_id = db.Column(db.String(50), default='')
    cost = db.Column(db.Numeric(5, 3))
    time_stamp = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
