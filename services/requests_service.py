from flask import Blueprint, request, jsonify
from google.cloud import firestore
from datetime import datetime

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint for requests
requests_bp = Blueprint('requests', __name__)

# Create a Request (POST)
@requests_bp.route('/', methods=['POST'])
def create_request():
    data = request.json
    student_id = data.get('student_id')
    request_type = data.get('type')
    details = data.get('details')

    if not student_id or not request_type or not details:
        return jsonify({"error": "Missing required data"}), 400

    request_data = {
        "student_id": student_id,
        "type": request_type,
        "details": details,
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
