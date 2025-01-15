from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
queues = {
    "first": {"queue_id": 1, "queue_name": "first", "players": []},
    "second": {"queue_id": 2, "queue_name": "second", "players": []},
    "third": {"queue_id": 3, "queue_name": "third", "players": []}
}

users_in_queue = {}

API_KEY = os.getenv("USERAGENT")

@app.route('/join_queue', methods=['POST'])
def join_queue():
    content_type = request.headers.get("Content-Type")
    if "application/x-www-form-urlencoded" not in content_type:
        return jsonify({"error": "Unauthorized, only Lua requests allowed."}), 401

    user = request.json.get('user')
    gamemode = request.json.get('gamemode')
    
    if not user or not gamemode:
        return jsonify({"message": "User and gamemode are required."}), 400
    
    if gamemode not in queues:
        return jsonify({"message": "Invalid gamemode."}), 400
    
    if user in users_in_queue:
        return jsonify({"message": f"{user} is already in a queue ({users_in_queue[user]})."}), 400

    queue = queues[gamemode]
    queue['players'].append(user)
    users_in_queue[user] = gamemode
    
    return jsonify({"message": f"{user} joined the {queue['queue_name']} queue.", "queue_id": queue['queue_id'], "queue_name": queue['queue_name']}), 200

@app.route('/leave_queue', methods=['POST'])
def leave_queue():
    content_type = request.headers.get("Content-Type")
    if "application/x-www-form-urlencoded" not in content_type:
        return jsonify({"error": "Unauthorized, only Lua requests allowed."}), 401

    user = request.json.get('user')
    gamemode = request.json.get('gamemode')
    
    if not user or not gamemode:
        return jsonify({"message": "User and gamemode are required."}), 400
    
    if gamemode not in queues:
        return jsonify({"message": "Invalid gamemode."}), 400
    
    queue = queues[gamemode]
    
    if user in queue['players']:
        queue['players'].remove(user)
        del users_in_queue[user]
        return jsonify({"message": f"{user} left the {queue['queue_name']} queue."}), 200
    
    return jsonify({"message": "User not found in the queue."}), 400

@app.route('/get_queue', methods=['GET'])
def get_queue():
    content_type = request.headers.get("Content-Type")
    if "application/x-www-form-urlencoded" not in content_type:
        return jsonify({"error": "Unauthorized, only Lua requests allowed."}), 401

    max_queue = max(queues.values(), key=lambda x: len(x['players']))
    return jsonify({"gamemode": max_queue['queue_name'], "queue_id": max_queue['queue_id'], "queue_name": max_queue['queue_name'], "players": len(max_queue['players'])}), 200

@app.route('/')
def home():
    content_type = request.headers.get("Content-Type")
    if "application/x-www-form-urlencoded" not in content_type:
        return jsonify({"error": "Unauthorized, only Lua requests allowed."}), 401

    return "API is Online and running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
