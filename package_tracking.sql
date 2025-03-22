-- Agents Table
CREATE TABLE Agents (
    agent_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- For authentication
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Packages Table
CREATE TABLE Packages (
    package_id INT AUTO_INCREMENT PRIMARY KEY,
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    warehouse_id INT NOT NULL,
    customer_id INT NOT NULL,
    status ENUM('Pending', 'Assigned', 'In Transit', 'Delivered', 'Failed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assigned_Packages Table
CREATE TABLE Assigned_Packages (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    agent_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES Packages(package_id),
    FOREIGN KEY (agent_id) REFERENCES Agents(agent_id)
);

-- Package_Status_Log Table
CREATE TABLE Package_Status_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    agent_id INT NOT NULL,
    status ENUM('Pending', 'Assigned', 'In Transit', 'Delivered', 'Failed') NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES Packages(package_id),
    FOREIGN KEY (agent_id) REFERENCES Agents(agent_id)
);