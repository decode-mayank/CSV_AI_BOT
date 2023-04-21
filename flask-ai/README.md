Reference - https://rest-apis-flask.teclado.com/docs/first_rest_api/getting_set_up/

# How to run server
flask run

# How to apply migrations
flask db init
flask db migrate
flask db upgrade

# If you already have migrations file in migrations folder then run below command
flask db stamp head
flask db migrate
flask db upgrade


# Flask server run on default port 5000
http://127.0.0.1:5000/