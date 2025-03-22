from passlib.hash import pbkdf2_sha256
from database import db

def signup(username, password, role="user"):
    user_id = f"org.couchdb.user:{username}"
    if user_id in db:
        print("User already exists.")
        return

    hashed_password = pbkdf2_sha256.hash(password)
    user_doc = {
        "_id": user_id,
        "name": username,
        "type": "user",
        "roles": [role],
        "password": hashed_password
    }
    db.save(user_doc)
    print("User created successfully.")

def login(username, password):
    user_id = f"org.couchdb.user:{username}"
    if user_id not in db:
        print("User not found.")
        return False

    user_doc = db[user_id]
    if pbkdf2_sha256.verify(password, user_doc["password"]):
        print("Login successful.")
        return True
    else:
        print("Invalid password.")
        return False

def change_role(username, new_role):
    user_id = f"org.couchdb.user:{username}"
    if user_id not in db:
        print("User not found.")
        return

    user_doc = db[user_id]
    user_doc["roles"] = [new_role]
    db.save(user_doc)
    print("User role updated successfully.")
