from flask import Blueprint, request, jsonify
from google.cloud import firestore
from datetime import datetime

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint for inquiries
inquiries_bp = Blueprint('inquiries', __name__)

# Submit Inquiry
@inquiries_bp.route('/', methods=['POST'])
def submit_inquiry():
    data = request.json
    student_id = data.get('student_id')
    message = data.get('message')

    if not student_id or not message:
        return jsonify({"error": "Missing student_id or message"}), 400

    inquiry_data = {
        "student_id": student_id,
        "message": message,
        "status": "Pending",
        "created_at": datetime.utcnow()
    }

    # Store the inquiry in Firestore
    inquiry_ref = db.collection('inquiries').add(inquiry_data)
    return jsonify({"id": inquiry_ref[1].id, "status": "Inquiry submitted"}), 201

# Get All Inquiries for a User
@inquiries_bp.route('/history', methods=['GET'])
def inquiry_history():
    user_id = request.args.get('user_id')
    inquiries = db.collection('inquiries').where('student_id', '==', user_id).stream()
    inquiry_list = [{"id": inq.id, **inq.to_dict()} for inq in inquiries]
    return jsonify(inquiry_list)
