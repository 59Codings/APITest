from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
queues = {
    "first": {"queue_id": 1, "queue_name": "first", "players": []},
    "second": {"queue_id": 2, "queue_name": "second", "players": []},
    "third": {"queue_id": 3, "queue_name": "third", "players": []}
}

users_in_first_queue = {}
users_in_second_queue = {}
users_in_third_queue = {}

ALLOWED_HEADER = os.getenv("ALLOWED_HEADER")

@app.route('/join_queue', methods=['POST'])
def join_queue():
    custom_header = request.headers.get("ALLOWEDorDev")
    
    if custom_header != ALLOWED_HEADER:
        return jsonify({"error": "Unauthorized"}), 401

    user = request.json.get('user')
    gamemode = request.json.get('gamemode')
    
    if not user or not gamemode:
        return jsonify({"message": "User and gamemode are required."}), 400
    
    if gamemode not in queues:
        return jsonify({"message": "Invalid gamemode."}), 400
    
    if gamemode == "first" and user in users_in_first_queue:
        return jsonify({"message": f"{user} is already in the first queue."}), 400
    elif gamemode == "second" and user in users_in_second_queue:
        return jsonify({"message": f"{user} is already in the second queue."}), 400
    elif gamemode == "third" and user in users_in_third_queue:
        return jsonify({"message": f"{user} is already in the third queue."}), 400

    queue = queues[gamemode]
    queue['players'].append(user)

    if gamemode == "first":
        users_in_first_queue[user] = gamemode
    elif gamemode == "second":
        users_in_second_queue[user] = gamemode
    elif gamemode == "third":
        users_in_third_queue[user] = gamemode
    
    return jsonify({"message": f"{user} joined the {queue['queue_name']} queue.", "queue_id": queue['queue_id'], "queue_name": queue['queue_name']}), 200

@app.route('/leave_queue', methods=['POST'])
def leave_queue():
    custom_header = request.headers.get("ALLOWEDorDev")
    
    if custom_header != ALLOWED_HEADER:
        return jsonify({"error": "Unauthorized"}), 401

    user = request.json.get('user')
    gamemode = request.json.get('gamemode')
    
    if not user or not gamemode:
        return jsonify({"message": "User and gamemode are required."}), 400
    
    if gamemode not in queues:
        return jsonify({"message": "Invalid gamemode."}), 400
    
    queue = queues[gamemode]
    
    if user in queue['players']:
        queue['players'].remove(user)
        
        if gamemode == "first":
            del users_in_first_queue[user]
        elif gamemode == "second":
            del users_in_second_queue[user]
        elif gamemode == "third":
            del users_in_third_queue[user]
        
        return jsonify({"message": f"{user} left the {queue['queue_name']} queue."}), 200
    
    return jsonify({"message": "User not found in the queue."}), 400

@app.route('/get_queue', methods=['GET'])
def get_queue():
    custom_header = request.headers.get("ALLOWEDorDev")
    
    if custom_header != ALLOWED_HEADER:
        return jsonify({"error": "Unauthorized"}), 401

    queue_name = request.args.get("queue")

    if not queue_name:
        return jsonify({"error": "Queue name is required."}), 400

    if queue_name in queues:
        queue = queues[queue_name]
        return jsonify({
            "gamemode": queue['queue_name'], 
            "queue_id": queue['queue_id'], 
            "queue_name": queue['queue_name'], 
            "players": len(queue['players'])
        }), 200
    
    return jsonify({"error": "Invalid queue name."}), 400

@app.route('/')
def home():
    return "API is Online and running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
