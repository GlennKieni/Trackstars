import couchdb
import json

# CouchDB connection setup
COUCHDB_URL = 'http://admin:admin@127.0.0.1:5984/'
DB_NAME = 'package_tracking'

def get_db():
    """Connect to CouchDB and return the database."""
    couch = couchdb.Server(COUCHDB_URL)
    if DB_NAME not in couch:
        print(f"Database '{DB_NAME}' not found!")
        exit(1)
    return couch[DB_NAME]

def get_users():
    """Fetch all users."""
    db = get_db()
    users = [
        {
            'id': doc_id,
            'name': doc.get('name'),
            'email': doc.get('email'),
            'role': doc.get('role', 'customer'),
            'status': doc.get('status', 'inactive')
        }
        for doc_id, doc in db.items() if doc.get('type') == 'user'
    ]

    print(json.dumps(users, indent=4))

def update_user_status(user_id):
    """Toggle user status between active and inactive."""
    db = get_db()
    user = db.get(user_id)
    if not user or user.get('type') != 'user':
        print("Invalid user ID.")
        return

    current_status = user.get('status', 'inactive')
    new_status = 'active' if current_status == 'inactive' else 'inactive'
    user['status'] = new_status
    db[user_id] = user

    print(f"User '{user_id}' status changed to '{new_status}'.")

def assign_role(user_id, new_role):
    """Assign a new role to a user."""
    valid_roles = ('admin', 'customer', 'delivery_agent')
    if new_role not in valid_roles:
        print(f"Invalid role. Choose from {valid_roles}.")
        return

    db = get_db()
    user = db.get(user_id)
    if not user or user.get('type') != 'user':
        print("Invalid user ID.")
        return

    user['role'] = new_role
    db[user_id] = user
    print(f"User '{user_id}' role changed to '{new_role}'.")

def generate_reports():
    """Generate reports on users and packages."""
    db = get_db()
    total_users = 0
    inactive_users = 0
    active_deliveries = 0
    pending_deliveries = 0

    for doc_id, doc in db.items():
        if doc.get('type') == 'user':
            total_users += 1
            if doc.get('status') == 'inactive':
                inactive_users += 1

        elif doc.get('type') == 'package':
            if doc.get('status') == 'in_transit':
                active_deliveries += 1
            elif doc.get('status') == 'pending':
                pending_deliveries += 1

    report = {
        "total_users": total_users,
        "inactive_users": inactive_users,
        "active_deliveries": active_deliveries,
        "pending_deliveries": pending_deliveries
    }

    print(json.dumps(report, indent=4))

def main():
    """CLI Menu."""
    while True:
        print("\n--- CouchDB Admin Menu ---")
        print("1. Get all users")
        print("2. Update user status (activate/deactivate)")
        print("3. Assign role to user")
        print("4. Generate reports")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            get_users()
        elif choice == '2':
            user_id = input("Enter user ID: ")
            update_user_status(user_id)
        elif choice == '3':
            user_id = input("Enter user ID: ")
            new_role = input("Enter new role (admin/customer/delivery_agent): ").lower()
            assign_role(user_id, new_role)
        elif choice == '4':
            generate_reports()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
