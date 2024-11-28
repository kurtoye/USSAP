from flask import Blueprint, request, jsonify
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

# Define Blueprint
inquiries_bp = Blueprint("inquiries", __name__)
inquiries_collection = db.collection("inquiries")

# Submit Inquiry (POST)
@inquiries_bp.route('/submit', methods=['POST'])
def submit_inquiry():
    data = request.json
    inquiry_ref = inquiries_collection.add({
        "student": data["student"],
        "message": data["message"],
        "status": "Pending"
    })
    return jsonify({"id": inquiry_ref[1].id, "status": "Inquiry submitted"}), 201

# Inquiry Status (GET)
@inquiries_bp.route('/status/<inquiry_id>', methods=['GET'])
def inquiry_status(inquiry_id):
    inquiry = inquiries_collection.document(inquiry_id).get()
    if inquiry.exists:
        return jsonify({
            "student": inquiry.to_dict()["student"],
            "message": inquiry.to_dict()["message"],
            "status": inquiry.to_dict()["status"]
        })
    return jsonify({"error": "Inquiry not found"}), 404

