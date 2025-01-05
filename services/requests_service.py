from flask import Blueprint, request, jsonify
from datetime import datetime
from config.firestore_client import db


# Define Blueprint
requests_bp = Blueprint('requests', __name__)

# Submit Request
@requests_bp.route('/', methods=['POST'])
def submit_request():
    try:
        data = request.json
        if not data or "student_id" not in data or "type" not in data or "details" not in data:
            return jsonify({"error": "Missing student_id, type, or details"}), 400

        request_data = {
            "student_id": str(data["student_id"]),
            "type": str(data["type"]),
            "details": str(data["details"]),
            "status": "Pending",
            "created_at": datetime.utcnow()
        }

        request_ref = db.collection('requests').add(request_data)
        return jsonify({"id": request_ref[1].id, "message": "Request created"}), 201
    except Exception as e:
        print(f"Error in submit_request: {e}")
        return jsonify({"error": "An error occurred while submitting the request"}), 500

# Get All Requests (Admin)
@requests_bp.route('/admin', methods=['GET'])
def get_all_requests():
    try:
        requests = db.collection('requests').stream()
        request_list = [{"id": req.id, **req.to_dict()} for req in requests]
        return jsonify(request_list), 200
    except Exception as e:
        print(f"Error in get_all_requests: {e}")
        return jsonify({"error": "An error occurred while fetching requests"}), 500

# Update Request Status (Admin)
@requests_bp.route('/admin/<request_id>', methods=['PUT'])
def update_request_status(request_id):
    try:
        data = request.json
        if not data or "status" not in data:
            return jsonify({"error": "Missing status"}), 400

        request_ref = db.collection('requests').document(request_id)
        if not request_ref.get().exists:
            return jsonify({"error": "Request not found"}), 404

        request_ref.update({"status": data["status"]})
        return jsonify({"message": "Request status updated"}), 200
    except Exception as e:
        print(f"Error in update_request_status: {e}")
        return jsonify({"error": "An error occurred while updating request status"}), 500

# Query Requests by Student ID or Status or Type
@requests_bp.route('/', methods=['GET'])
def get_requests_by_filters():
    try:
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        request_type = request.args.get('type')

        query = db.collection('requests')
        if student_id:
            query = query.where('student_id', '==', student_id)
        if status:
            query = query.where('status', '==', status)
        if request_type:
            query = query.where('type', '==', request_type)

        requests = query.stream()
        request_list = [{"id": req.id, **req.to_dict()} for req in requests]
        return jsonify(request_list), 200
    except Exception as e:
        print(f"Error in get_requests_by_filters: {e}")
        return jsonify({"error": "An error occurred while querying requests"}), 500

# Delete a Request (Admin)
@requests_bp.route('/admin/<request_id>', methods=['DELETE'])
def delete_request(request_id):
    try:
        request_ref = db.collection('requests').document(request_id)
        if not request_ref.get().exists:
            return jsonify({"error": "Request not found"}), 404

        request_ref.delete()
        return jsonify({"message": "Request deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_request: {e}")
        return jsonify({"error": f"Failed to process inquiry: {str(e)}"}), 500

