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
    # return jsonify({"message": "Hello, Flask is running with Firestore"})

# # Example POST Endpoint
# @app.route('/submit', methods=['POST'])
# def submit_data():
#     data = request.json
#     return jsonify({"received": data}), 201

# Submit Inquiry (POST)
#@app.route('/submit_inquiry', methods=['POST'])


# # Inquiry Status (GET)
# @app.route('/inquiry_status/<inquiry_id>', methods=['GET'])


# # Create Request (POST)
# @app.route('/requests', methods=['POST'])


# # Get All Requests (GET)
# @app.route('/requests', methods=['GET'])
# def get_all_requests():
#     requests = requests_collection.stream()  # Fetch all documents
#     request_list = []



#       missing
#     for req in requests:
#         req_data = req.to_dict()
#         req_data["id"] = req.id
#         request_list.append(req_data)



#     return jsonify(request_list), 200

# # Get Request by ID (GET)
# @app.route('/requests/<request_id>', methods=['GET'])
# def get_request_by_id(request_id):
#     req = requests_collection.document(request_id).get()
#     if req.exists:
#         req_data = req.to_dict()
#         req_data["id"] = req.id
#         return jsonify(req_data), 200
#     return jsonify({"error": "Request not found"}), 404

# # Update Request (PUT)
# @app.route('/requests/<request_id>', methods=['PUT'])
# def update_request(request_id):
#     data = request.get_json()
#     if "status" not in data:
#         return jsonify({"error": "Status field is required"}), 400

#     result = requests_collection.document(request_id).update({"status": data["status"]})

#     return jsonify({"message": "Request updated"}), 200

# # Delete Request (DELETE)
# @app.route('/requests/<request_id>', methods=['DELETE'])
# def delete_request(request_id):
#     requests_collection.document(request_id).delete()
#     return jsonify({"message": "Request deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
