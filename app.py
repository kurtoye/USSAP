import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp

# Initialize Firebase
# cred = credentials.Certificate('graceful-cider-438814-e0-firebase-adminsdk-8958u-a2289d9f51.json')  # Update the filepath here
# firebase_admin.initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)

# Register Blueprints for routes
app.register_blueprint(inquiries_bp, url_prefix='/inquiries')
app.register_blueprint(requests_bp, url_prefix='/requests')

# Routes

# Home Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the University Student Support API"})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    token = request.json.get("token")  # Get the token from frontend
    try:
        decoded_token = auth.verify_id_token(token)  # Verify Firebase token
        user_id = decoded_token['uid']  # Get the user ID from the token
        return jsonify({"message": "Login successful", "user_id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Dashboard Route
@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = request.args.get('user_id')
    # Query Firestore for user data or simply use static data for testing
    user_data = {"user_name": "John Doe", "inquiries": ["Inquiry 1", "Inquiry 2"]}
    return jsonify(user_data)

# Inquiry History Route (Newly added without the chatbot logic)
@app.route('/inquiry-history', methods=['GET'])
def inquiry_history():
    # Retrieve inquiry history from Firestore or other database (mock example)
    user_id = request.args.get('user_id')
    inquiries = [
        {"inquiry_id": 1, "message": "What is the registration deadline?", "status": "Pending"},
        {"inquiry_id": 2, "message": "How can I apply for financial aid?", "status": "Resolved"}
    ]
    return jsonify({"user_id": user_id, "inquiries": inquiries})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
