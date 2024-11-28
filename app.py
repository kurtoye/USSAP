from flask import Flask, request, jsonify
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp
# from google.cloud import firestore  # Import Firestore SDK

# Initialize Flask app
app = Flask(__name__)

# Reference to collections in Firestore
inquiries_collection = db.collection("inquiries")
requests_collection = db.collection("requests")

#changed 
app.register_blueprint(inquiries_bp, url_prefix="/inquiries")
app.register_blueprint(requests_bp, url_prefix="/requests")

# Root Route
@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the University Student Support API"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
