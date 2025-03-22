import sqlite3
from datetime import datetime

# Database connection
DATABASE = 'package_tracking.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Task 1: Assign packages to delivery agents
def assign_package_to_agent(package_id, agent_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the package is already assigned
    cursor.execute('SELECT status FROM Packages WHERE package_id = ?', (package_id,))
    package = cursor.fetchone()
    if package and package['status'] == 'Assigned':
        return "Package is already assigned."

    # Assign package to agent
    cursor.execute('''
        INSERT INTO Assigned_Packages (package_id, agent_id)
        VALUES (?, ?)
    ''', (package_id, agent_id))

    # Update package status
    cursor.execute('''
        UPDATE Packages
        SET status = 'Assigned'
        WHERE package_id = ?
    ''', (package_id,))

    conn.commit()
    conn.close()
    return "Package assigned successfully."

# Task 2: Fetch list of assigned packages per agent
def get_assigned_packages(agent_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.package_id, p.tracking_number, p.status, a.assigned_at
        FROM Packages p
        JOIN Assigned_Packages a ON p.package_id = a.package_id
        WHERE a.agent_id = ?
    ''', (agent_id,))
    packages = cursor.fetchall()

    conn.close()
    return packages

# Task 3: Allow agents to update package status
def update_package_status(package_id, agent_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the agent is authorized to update this package
    cursor.execute('''
        SELECT agent_id FROM Assigned_Packages
        WHERE package_id = ?
    ''', (package_id,))
    assignment = cursor.fetchone()
    if not assignment or assignment['agent_id'] != agent_id:
        return "Unauthorized update."

    # Update package status
    cursor.execute('''
        UPDATE Packages
        SET status = ?
        WHERE package_id = ?
    ''', (status, package_id))

    # Log the status update
    cursor.execute('''
        INSERT INTO Package_Status_Log (package_id, agent_id, status)
        VALUES (?, ?, ?)
    ''', (package_id, agent_id, status))

    conn.commit()
    conn.close()
    return "Package status updated successfully."

# Task 4: Prevent unauthorized updates (handled in update_package_status)

# Example usage
if __name__ == "__main__":
    # Assign package 1 to agent 1
    print(assign_package_to_agent(1, 1))

    # Fetch assigned packages for agent 1
    packages = get_assigned_packages(1)
    for package in packages:
        print(package)

    # Update package status
    print(update_package_status(1, 1, 'In Transit'))