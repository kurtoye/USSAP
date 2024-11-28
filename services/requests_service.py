from flask import Blueprint, request, jsonify
from google.cloud import firestore
<<<<<<< HEAD
=======
from datetime import datetime
>>>>>>> 473f8e2fcb236b6b92c1fba83b220230d6582a5b

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint
<<<<<<< HEAD
requests_bp = Blueprint("requests", __name__)
requests_collection = db.collection("requests")

# Create Request (POST)
@requests_bp.route('/', methods=['POST'])
def create_request():
    data = request.get_json()
    if not all(key in data for key in ["student_id", "name", "request", "status"]):
        return jsonify({"error": "Missing data"}), 400
    result = requests_collection.add(data)
    return jsonify({"message": "Request created", "id": result[1].id}), 201

# Get All Requests
@requests_bp.route('/', methods=['GET'])
def get_all_requests():
    requests = requests_collection.stream()
    request_list = [{"id": req.id, **req.to_dict()} for req in requests]
    return jsonify(request_list), 200
=======
requests_bp = Blueprint('requests', __name__)

# Create Request
@requests_bp.route('/', methods=['POST'])
def create_request():
    data = request.json
    if not data or "student_id" not in data or "type" not in data or "details" not in data:
        return jsonify({"error": "Missing student_id, type, or details"}), 400

    request_data = {
        "student_id": data["student_id"],
        "type": data["type"],
        "details": data["details"],
        "status": "Pending",
        "created_at": datetime.utcnow()
    }
    request_ref = db.collection('requests').add(request_data)
    return jsonify({"id": request_ref[1].id, "message": "Request created"}), 201

# Get All Requests (Admin)
@requests_bp.route('/admin', methods=['GET'])
def get_all_requests():
    requests = db.collection('requests').stream()
    request_list = [{"id": req.id, **req.to_dict()} for req in requests]
    return jsonify(request_list), 200

# Update Request Status (Admin)
@requests_bp.route('/admin/<request_id>', methods=['PUT'])
def update_request_status(request_id):
    data = request.json
    if not data or "status" not in data:
        return jsonify({"error": "Missing status"}), 400

    request_ref = db.collection('requests').document(request_id)
    if not request_ref.get().exists:
        return jsonify({"error": "Request not found"}), 404

    request_ref.update({"status": data["status"]})
    return jsonify({"message": "Request status updated"}), 200
>>>>>>> 473f8e2fcb236b6b92c1fba83b220230d6582a5b
