from flask import Flask, request, jsonify
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp
# from google.cloud import firestore  # Import Firestore SDK

db = firestore.Client()

# Initialize Flask app
app = Flask(__name__)


# Register Blueprints 
app.register_blueprint(inquiries_bp, url_prefix="/inquiries")
app.register_blueprint(requests_bp, url_prefix="/requests")

# Root Route
@app.route('/', methods=['GET'])
def home():
<<<<<<< HEAD
    return {"message": "Welcome to the University Student Support API"}
=======
    return jsonify({"message": "Hello, Flask is running with Firestore provisionally"})
>>>>>>> 473f8e2fcb236b6b92c1fba83b220230d6582a5b


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
