from flask import Flask, jsonify
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp

import firebase_admin
from firebase_admin import credentials, auth

# Initialse Firebase Authentication
cred = credentials.Certificate ('graceful-cider-438814-e0-firebase-adminsdk-8958u-a2289d9f51')
firebase_admin.initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(inquiries_bp, url_prefix='/inquiries')
app.register_blueprint(requests_bp, url_prefix='/requests')

# Root Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "University Student Support API"})

# Debugging Tip: Print all routes
print(app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
