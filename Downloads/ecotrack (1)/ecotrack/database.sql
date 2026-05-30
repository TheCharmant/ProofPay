CREATE DATABASE IF NOT EXISTS ecotrack_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ecotrack_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    points INT DEFAULT 0,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity_feeds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    barangay VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    activity_type ENUM('cleanup_drive', 'environmental_education', 'tree_planting', 'other') NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    image_url VARCHAR(255),
    status ENUM('upcoming', 'ongoing', 'completed') DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    barangay VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    location_notes TEXT,
    issue_type ENUM('uncollected_garbage', 'illegal_dumping', 'overflowing_bin', 'littering', 'other') NOT NULL,
    status ENUM('pending', 'in_progress', 'resolved') DEFAULT 'pending',
    admin_notes TEXT,
    resolution_notes TEXT,
    points_awarded INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS report_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    image_type ENUM('report', 'resolution') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    barangay VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    activity_type ENUM('cleanup_drive', 'environmental_education', 'tree_planting', 'other') NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    points_reward INT DEFAULT 10,
    image_url VARCHAR(255),
    status ENUM('upcoming', 'ongoing', 'completed') DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    user_id INT NOT NULL,
    points_awarded INT DEFAULT 0,
    status ENUM('registered', 'attended', 'completed') DEFAULT 'registered',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_participant (activity_id, user_id)
);

CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_by INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO users (name, email, password, role, points) VALUES 
('Admin', 'admin@ecotrack.com', SHA2('admin123', 256), 'admin', 0)
ON DUPLICATE KEY UPDATE name=name;

INSERT INTO users (name, email, password, role, points) VALUES 
('Juan dela Cruz', 'user@ecotrack.com', SHA2('user123', 256), 'user', 50)
ON DUPLICATE KEY UPDATE name=name;

INSERT INTO reports (user_id, title, description, barangay, location, location_notes, issue_type, status) 
SELECT u.id, 'Overflowing bin near market', 'The trash bin near the public market has been overflowing for 3 days.', 'Asinan', 'Public Market, Main St.', 'Near the main entrance', 'overflowing_bin', 'pending'
FROM users u WHERE u.email='user@ecotrack.com' LIMIT 1;

INSERT INTO reports (user_id, title, description, barangay, location, location_notes, issue_type, status) 
SELECT u.id, 'Illegal dumping at riverbank', 'Large piles of construction waste illegally dumped near the river.', 'Gordon Heights', 'Riverbank', 'Behind the residential area', 'illegal_dumping', 'in_progress'
FROM users u WHERE u.email='user@ecotrack.com' LIMIT 1;

INSERT INTO reports (user_id, title, description, barangay, location, location_notes, issue_type, status) 
SELECT u.id, 'Uncollected garbage on Rizal Ave', 'Garbage has not been collected for over a week on this street.', 'Kalaklan', 'Rizal Avenue, Block 4', 'Corner intersection', 'uncollected_garbage', 'resolved'
FROM users u WHERE u.email='user@ecotrack.com' LIMIT 1;