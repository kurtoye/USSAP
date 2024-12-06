from flask import Flask, jsonify
from services.inquiries_service import inquiries_bp
from services.requests_service import requests_bp
>>>>>>> d1e1399fa0a83d501a93bdceb430038885f91d51

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
