from flask import Flask, jsonify
from flask import request
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp
from services.chatbot_services import get_chatbot_response
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


api_key = os.getenv('OPENAI_API_KEY')
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Validate environment variables
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment.")
if not credentials_path or not os.path.exists(credentials_path):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is missing or invalid.")

# Initialize Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(inquiries_bp, url_prefix='/inquiries')
app.register_blueprint(requests_bp, url_prefix='/requests')

# Root Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "University Student Support API"})


@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        if 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        response = get_chatbot_response(user_message) or "No response generated."
        
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"Error in chatbot endpoint: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
# Debugging Tip: Print all routes
print(app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
