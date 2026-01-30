-- Create database
CREATE DATABASE IF NOT EXISTS e_ration_db;
USE e_ration_db;

-- ----------------------------
-- Users table (Citizen)
-- ----------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Admin table
-- ----------------------------
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert default admin
-- Password = admin123 (hashed example)
INSERT INTO admin (username, password)
VALUES (
    'admin',
    '$pbkdf2-sha256$260000$examplehash'
);

-- ----------------------------
-- Ration items table
-- ----------------------------
CREATE TABLE ration_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    quantity VARCHAR(50) NOT NULL
);

-- ----------------------------
-- User ration allocation
-- ----------------------------
CREATE TABLE user_ration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT,
    month_year VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Not Collected',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES ration_items(id)
);

