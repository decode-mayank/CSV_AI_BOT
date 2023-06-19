from flask import Flask, request, jsonify
from config import CONNECTION_STRING
from bot import generate_response


# Create Flask application instance
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['user_message']
    # Get user's message from JSON request
    response = generate_response(user_message)
    
    return jsonify({'responses': response})

if __name__ == "__main__":
    app.run(debug=True)