from flask import Blueprint, request, jsonify
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint
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
