from flask import Blueprint, request, jsonify
from google.cloud import firestore
from datetime import datetime

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint
inquiries_bp = Blueprint('inquiries', __name__)

# Submit Inquiry
@inquiries_bp.route('/', methods=['POST'])
def submit_inquiry():
    try:
        # Parse request data
        data = request.get_json()
        if not data or "student_id" not in data or "message" not in data:
            return jsonify({"error": "Missing student_id or message"}), 400

        # Prepare Firestore document
        inquiry_data = {
            "student_id": str(data["student_id"]),  # Ensure data consistency
            "message": str(data["message"]),
            "status": "Pending",
            "priority": "Normal",
            "created_at": firestore.SERVER_TIMESTAMP  # Use Firestore's server timestamp
        }

        # Add to Firestore collection
        inquiry_ref = db.collection('inquiries').add(inquiry_data)

        # Return response
        return jsonify({"id": inquiry_ref[1].id, "message": "Inquiry submitted"}), 201
    except Exception as e:
        print(f"Error in submit_inquiry: {e}")
        return jsonify({"error": "An error occurred while submitting the inquiry"}), 500

# Get All Inquiries (Admin)
@inquiries_bp.route('/admin', methods=['GET'])
def get_all_inquiries():
    try:
        inquiries = db.collection('inquiries').stream()
        inquiry_list = [{"id": inq.id, **inq.to_dict()} for inq in inquiries]
        return jsonify(inquiry_list), 200
    except Exception as e:
        print(f"Error in get_all_inquiries: {e}")
        return jsonify({"error": "An error occurred while fetching inquiries"}), 500

# Update Inquiry Status (Admin)
@inquiries_bp.route('/admin/<inquiry_id>', methods=['PUT'])
def update_inquiry_status(inquiry_id):
    try:
        data = request.get_json()
        if not data or "status" not in data:
            return jsonify({"error": "Missing status"}), 400

        inquiry_ref = db.collection('inquiries').document(inquiry_id)
        if not inquiry_ref.get().exists:
            return jsonify({"error": "Inquiry not found"}), 404

        inquiry_ref.update({"status": data["status"]})
        return jsonify({"message": "Inquiry status updated"}), 200
    except Exception as e:
        print(f"Error in update_inquiry_status: {e}")
        return jsonify({"error": "An error occurred while updating inquiry status"}), 500