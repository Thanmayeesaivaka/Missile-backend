from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['missile']
users_collection = db['users']
topics_collection = db['start']

# ----------------------------
# User Login API
# ----------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email})
    if user and user['password'] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# ----------------------------
# User Register API
# ----------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'Email already registered'}), 400

    users_collection.insert_one({'email': email, 'password': password})
    return jsonify({'message': 'Registration successful'}), 201

# ----------------------------
# Topic Fetch API
# ----------------------------
@app.route('/api/topic/<topic>', methods=['GET'])
def get_topic(topic):
    topic_doc = topics_collection.find_one({'topic': topic})
    if topic_doc:
        response = {
            'title': topic_doc.get('title', ''),
            'description': topic_doc.get('description', ''),
            'buttons': topic_doc.get('buttons', []),
            'content': topic_doc.get('content', [])
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Topic not found'}), 404

# ----------------------------
# Run the Flask app
# ----------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
