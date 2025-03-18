from passlib.hash import pbkdf2_sha256  # Make sure this is imported at the top
from flask import Blueprint, request, jsonify
from database import db
from passlib.hash import pbkdf2_sha256

auth_routes = Blueprint('auth_routes', __name__)

# User Signup Route
@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")  # Default role is "user"

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user_id = f"org.couchdb.user:{username}"

    if user_id in db:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = pbkdf2_sha256.hash(password)

    user_doc = {
        "_id": user_id,
        "name": username,
        "type": "user",
        "roles": [role],
        "password": hashed_password
    }

    db.save(user_doc)
    return jsonify({"message": "User created successfully"}), 201


# User Login Route
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user_id = f"org.couchdb.user:{username}"

    if user_id not in db:
        return jsonify({"error": "User not found"}), 404

    user_doc = db[user_id]

    if pbkdf2_sha256.verify(password, user_doc["password"]):
        return jsonify({"message": "Login successful", "role": user_doc["roles"]}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


# Change User Role
@auth_routes.route('/change-role', methods=['POST'])
def change_role():
    data = request.json
    username = data.get("username")
    new_role = data.get("role")

    if not username or not new_role:
        return jsonify({"error": "Username and new role required"}), 400

    user_id = f"org.couchdb.user:{username}"

    if user_id not in db:
        return jsonify({"error": "User not found"}), 404

    user_doc = db[user_id]
    user_doc["roles"] = [new_role]
    db.save(user_doc)

    return jsonify({"message": "User role updated successfully"}), 200
