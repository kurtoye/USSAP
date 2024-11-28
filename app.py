from flask import Flask, request, jsonify
from google.cloud import firestore  # Import Firestore SDK

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client()

# Reference to collections in Firestore
inquiries_collection = db.collection("inquiries")
requests_collection = db.collection("requests")

# Root Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello, Flask is running with Firestore provisionally"})

# Example POST Endpoint
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    return jsonify({"received": data}), 201

# Submit Inquiry (POST)
@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    data = request.json
    inquiry_ref = inquiries_collection.add({
        "student": data["student"],
        "message": data["message"],
        "status": "Pending"
    })
    return jsonify({"id": inquiry_ref.id, "status": "Inquiry submitted"}), 201

# Inquiry Status (GET)
@app.route('/inquiry_status/<inquiry_id>', methods=['GET'])
def inquiry_status(inquiry_id):
    inquiry = inquiries_collection.document(inquiry_id).get()
    if inquiry.exists:
        return jsonify({
            "student": inquiry.to_dict()["student"],
            "message": inquiry.to_dict()["message"],
            "status": inquiry.to_dict()["status"]
        })
    return jsonify({"error": "Inquiry not found"}), 404

# Create Request (POST)
@app.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    if not all(key in data for key in ["student_id", "name", "request", "status"]):
        return jsonify({"error": "Missing data"}), 400

    result = requests_collection.add(data)
    return jsonify({"message": "Request created", "id": result.id}), 201

# Get All Requests (GET)
@app.route('/requests', methods=['GET'])
def get_all_requests():
    requests = requests_collection.stream()  # Fetch all documents
    request_list = []
    for req in requests:
        req_data = req.to_dict()
        req_data["id"] = req.id
        request_list.append(req_data)
    return jsonify(request_list), 200

# Get Request by ID (GET)
@app.route('/requests/<request_id>', methods=['GET'])
def get_request_by_id(request_id):
    req = requests_collection.document(request_id).get()
    if req.exists:
        req_data = req.to_dict()
        req_data["id"] = req.id
        return jsonify(req_data), 200
    return jsonify({"error": "Request not found"}), 404

# Update Request (PUT)
@app.route('/requests/<request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json()
    if "status" not in data:
        return jsonify({"error": "Status field is required"}), 400

    result = requests_collection.document(request_id).update({"status": data["status"]})

    return jsonify({"message": "Request updated"}), 200

# Delete Request (DELETE)
@app.route('/requests/<request_id>', methods=['DELETE'])
def delete_request(request_id):
    requests_collection.document(request_id).delete()
    return jsonify({"message": "Request deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
