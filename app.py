from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["university_support"]
inquiries_collection = db["inquiries"]
collection = db["requests"]

# OpenAI Setup
openai.api_key = "YOUR_OPENAI_API_KEY"

# Root Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello, Flask is running locally"})

# Example POST Endpoint
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    return jsonify({"received": data}), 201

# Submit Inquiry (POST)
@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    data = request.json
    inquiry_id = inquiries_collection.insert_one({
        "student": data["student"],
        "message": data["message"],
        "status": "Pending"
    }).inserted_id
    return jsonify({"id": str(inquiry_id), "status": "Inquiry submitted"}), 201

# Inquiry Status (GET)
@app.route('/inquiry_status/<int:id>', methods=['GET'])
def inquiry_status(id):
    inquiry = inquiries_collection.find_one({"_id": ObjectId(id)})
    if inquiry:
        return jsonify({
            "student": inquiry["student"],
            "message": inquiry["message"],
            "status": inquiry["status"]
        })
    return jsonify({"error": "Inquiry not found"}), 404

# Create Request (POST)
@app.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    if not all(key in data for key in ["student_id", "name", "request", "status"]):
        return jsonify({"error": "Missing data"}), 400

    result = collection.insert_one(data)
    return jsonify({"message": "Request created", "id": str(result.inserted_id)}), 201

# Get All Requests (GET)
@app.route('/requests', methods=['GET'])
def get_all_requests():
    requests = list(collection.find())  # Convert cursor to list
    for req in requests:
        req["_id"] = str(req["_id"])
    return jsonify(requests), 200

# Get Request by ID (GET)
@app.route('/requests/<request_id>', methods=['GET'])
def get_request_by_id(request_id):
    req = collection.find_one({"_id": ObjectId(request_id)})
    if req is None:
        return jsonify({"error": "Request not found"}), 404
    req["_id"] = str(req["_id"])
    return jsonify(req), 200

# Update Request (PUT)
@app.route('/requests/<request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json()
    if "status" not in data:
        return jsonify({"error": "Status field is required"}), 400

    result = collection.update_one(
        {"_id": ObjectId(request_id)}, 
        {"$set": {"status": data["status"]}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Request not found"}), 404

    return jsonify({"message": "Request updated"}), 200

# Delete Request (DELETE)
@app.route('/requests/<request_id>', methods=['DELETE'])
def delete_request(request_id):
    result = collection.delete_one({"_id": ObjectId(request_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Request not found"}), 404
    return jsonify({"message": "Request deleted"}), 200

# Process Inquiry with OpenAI (GET)
@app.route('/process_inquiry/<int:id>', methods=['GET'])
def process_inquiry(id):
    inquiry = inquiries_collection.find_one({"_id": ObjectId(id)})
    if not inquiry:
        return jsonify({"error": "Inquiry not found"}), 404

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Respond to this inquiry: {inquiry['message']}",
        max_tokens=100
    )
    return jsonify({"response": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)
