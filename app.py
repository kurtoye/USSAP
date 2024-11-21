from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
from bson import ObjectId
from bson.errors import InvalidId

# Initialize Flask app
app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  # Change to your MongoDB URI if needed
db = client["university_support"]
inquiries_collection = db["inquiries"]
requests_collection = db["requests"]

# OpenAI Setup
openai.api_key = "YOUR_OPENAI_API_KEY"

# Root Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello, Flask is running locally"}), 200

# Submit Inquiry (POST)
@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    try:
        data = request.json
        if not all(key in data for key in ["student", "message"]):
            return jsonify({"error": "Missing required fields: 'student', 'message'"}), 400
        
        inquiry_id = inquiries_collection.insert_one({
            "student": data["student"],
            "message": data["message"],
            "status": "Pending"
        }).inserted_id
        return jsonify({"id": str(inquiry_id), "status": "Inquiry submitted"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Inquiry Status (GET)
@app.route('/inquiry_status/<id>', methods=['GET'])
def inquiry_status(id):
    try:
        inquiry = inquiries_collection.find_one({"_id": ObjectId(id)})
        if not inquiry:
            return jsonify({"error": "Inquiry not found"}), 404
        return jsonify({
            "student": inquiry["student"],
            "message": inquiry["message"],
            "status": inquiry["status"]
        }), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Create Request (POST)
@app.route('/requests', methods=['POST'])
def create_request():
    try:
        data = request.json
        if not all(key in data for key in ["student_id", "name", "request", "status"]):
            return jsonify({"error": "Missing required fields"}), 400
        
        result = requests_collection.insert_one(data)
        return jsonify({"message": "Request created", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get All Requests (GET)
@app.route('/requests', methods=['GET'])
def get_all_requests():
    try:
        requests = list(requests_collection.find())
        for req in requests:
            req["_id"] = str(req["_id"])
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Get Request by ID (GET)
@app.route('/requests/<id>', methods=['GET'])
def get_request_by_id(id):
    try:
        request_data = requests_collection.find_one({"_id": ObjectId(id)})
        if not request_data:
            return jsonify({"error": "Request not found"}), 404
        request_data["_id"] = str(request_data["_id"])
        return jsonify(request_data), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Update Request (PUT)
@app.route('/requests/<id>', methods=['PUT'])
def update_request(id):
    try:
        data = request.json
        if "status" not in data:
            return jsonify({"error": "Missing 'status' field"}), 400
        
        result = requests_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"status": data["status"]}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Request not found"}), 404
        return jsonify({"message": "Request updated"}), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Delete Request (DELETE)
@app.route('/requests/<id>', methods=['DELETE'])
def delete_request(id):
    try:
        result = requests_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Request not found"}), 404
        return jsonify({"message": "Request deleted"}), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Process Inquiry with OpenAI (GET)
@app.route('/process_inquiry/<id>', methods=['GET'])
def process_inquiry(id):
    try:
        inquiry = inquiries_collection.find_one({"_id": ObjectId(id)})
        if not inquiry:
            return jsonify({"error": "Inquiry not found"}), 404
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Respond to this inquiry: {inquiry['message']}",
            max_tokens=100
        )
        return jsonify({"response": response.choices[0].text.strip()}), 200
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)