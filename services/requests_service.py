from flask import Blueprint, request, jsonify
from google.cloud import firestore
from datetime import datetime

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint
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
