from flask import Flask, request, jsonify
import sqlite3
import subprocess
import hashlib
import os
import shlex
import ast

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-12345")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password_hash))

    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "success", "user": username})

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    host = data.get("host", "")

    if not host.replace(".", "").isalnum():
        return jsonify({"error": "Invalid host"}), 400

   
    cmd = ["ping", "-c", "1", host]

    try:
        output = subprocess.check_output(cmd, timeout=3)
        return jsonify({"output": output.decode()})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Ping failed"}), 500



@app.route("/compute", methods=["POST"])
def compute():
    data = request.get_json()
    expression = data.get("expression", "1+1")

    try:
        
        result = ast.literal_eval(expression)
        return jsonify({"result": result})
    except Exception:
        return jsonify({"error": "Invalid expression"}), 400



@app.route("/hash", methods=["POST"])
def hash_password():
    data = request.get_json()
    pwd = data.get("password")

    
    hashed = hashlib.sha256(pwd.encode()).hexdigest()
    return jsonify({"sha256": hashed})



@app.route("/readfile", methods=["POST"])
def readfile():
    data = request.get_json()
    filename = data.get("filename")

    BASE_DIR = "files"
    safe_path = os.path.join(BASE_DIR, os.path.basename(filename))

    if not os.path.isfile(safe_path):
        return jsonify({"error": "File not found"}), 404

    with open(safe_path, "r") as f:
        content = f.read()

    return jsonify({"content": content})



@app.route("/debug", methods=["GET"])
def debug():
    return jsonify({"debug": False}), 403


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to the secure DevSecOps API"})


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=False)
