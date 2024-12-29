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
        data = request.json
        print(f"Received data: {data}")  # Debugging: log the received data
        
        # Validate the request payload
        if not data or "student_id" not in data or "message" not in data:
            return jsonify({"error": "Missing student_id or message"}), 400

        # Prepare inquiry data with correct types
        inquiry_data = {
            "student_id": str(data["student_id"]),  # Ensure student_id is stored as a string
            "message": str(data["message"]),       # Ensure message is stored as a string
            "status": "Pending",                   # Default status
            "priority": "Normal",                  # Default priority
            "created_at": datetime.utcnow()        # Use Firestore's native timestamp type
        }

        # Add the inquiry to Firestore
        inquiry_ref = db.collection('inquiries').add(inquiry_data)

        # Respond with the document ID and success message
        return jsonify({"id": inquiry_ref[1].id, "message": "Inquiry submitted"}), 201

    except Exception as e:
        # Log any exception for debugging purposes
        print(f"Error submitting inquiry: {e}")
        return jsonify({"error": "An error occurred while submitting the inquiry"}), 500

# Get All Inquiries (Admin)
@inquiries_bp.route('/admin', methods=['GET'])
def get_all_inquiries():
    try:
        inquiries = db.collection('inquiries').stream()
        inquiry_list = [{"id": inq.id, **inq.to_dict()} for inq in inquiries]
        return jsonify(inquiry_list), 200
    except Exception as e:
        print(f"Error fetching inquiries: {e}")
        return jsonify({"error": "An error occurred while fetching inquiries"}), 500

# Update Inquiry Status (Admin)
@inquiries_bp.route('/admin/<inquiry_id>', methods=['PUT'])
def update_inquiry_status(inquiry_id):
    try:
        data = request.json
        if not data or "status" not in data:
            return jsonify({"error": "Missing status"}), 400

        inquiry_ref = db.collection('inquiries').document(inquiry_id)
        if not inquiry_ref.get().exists:
            return jsonify({"error": "Inquiry not found"}), 404

        inquiry_ref.update({"status": data["status"]})
        return jsonify({"message": "Inquiry status updated"}), 200
    except Exception as e:
        print(f"Error updating inquiry status: {e}")
        return jsonify({"error": "An error occurred while updating inquiry status"}), 500
