Reference - https://rest-apis-flask.teclado.com/docs/first_rest_api/getting_set_up/

# How to run server
flask run

# If migrations folder not exist in the project
flask db init

# How to apply migrations
flask db migrate -m "Initial migration."
flask db upgrade

# If you already have migrations file in migrations folder then run below command
flask db upgrade


# Flask server run on default port 5000
http://127.0.0.1:5000/