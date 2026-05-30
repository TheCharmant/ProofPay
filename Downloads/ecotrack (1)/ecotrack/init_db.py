"""
EcoTrack — Database Initializer
Run this once before starting the app:  python init_db.py
"""

import mysql.connector
import hashlib
import sys

# CONFIG
HOST     = 'localhost'
USER     = 'root'
PASSWORD = ''
DB_NAME  = 'ecotrack_db'

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def run():
    print("EcoTrack — Database Setup")
    print("-" * 40)

    # 1. Connect without selecting a DB
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        print("[OK] Connected to MySQL")
    except mysql.connector.Error as e:
        print(f"[ERROR] Cannot connect to MySQL: {e}")
        print("Make sure XAMPP MySQL is running and credentials are correct.")
        sys.exit(1)

    # 2. Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE `{DB_NAME}`")
    print(f"[OK] Database '{DB_NAME}' ready")

    # 3. Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            name       VARCHAR(100) NOT NULL,
            email      VARCHAR(150) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            role       ENUM('user','admin') DEFAULT 'user',
            points     INT DEFAULT 0,
            bio        TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 4. Create reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            user_id         INT NOT NULL,
            title           VARCHAR(200) NOT NULL,
            description     TEXT NOT NULL,
            barangay        VARCHAR(100) NOT NULL,
            location        VARCHAR(255) NOT NULL,
            location_notes  TEXT,
            issue_type      ENUM('uncollected_garbage','illegal_dumping','overflowing_bin','littering','other') NOT NULL,
            status          ENUM('pending','in_progress','resolved') DEFAULT 'pending',
            admin_notes     TEXT,
            resolution_notes TEXT,
            points_awarded  INT DEFAULT 0,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 5. Create report_images table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS report_images (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            report_id  INT NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            image_type ENUM('report', 'resolution') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
        )
    """)

    # 6. Create activities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            admin_id      INT NOT NULL,
            title         VARCHAR(200) NOT NULL,
            description   TEXT NOT NULL,
            barangay      VARCHAR(100) NOT NULL,
            location      VARCHAR(255) NOT NULL,
            activity_type ENUM('cleanup_drive','environmental_education','tree_planting','other') NOT NULL,
            start_date    DATETIME NOT NULL,
            end_date      DATETIME,
            points_reward INT DEFAULT 10,
            image_url     VARCHAR(255),
            status        ENUM('upcoming','ongoing','completed') DEFAULT 'upcoming',
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 7. Create activity_participants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_participants (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            activity_id    INT NOT NULL,
            user_id        INT NOT NULL,
            points_awarded INT DEFAULT 0,
            status         ENUM('registered','attended','completed') DEFAULT 'registered',
            joined_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_participant (activity_id, user_id)
        )
    """)

    # 8. Create activity_feeds table (for admin posts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_feeds (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            admin_id      INT NOT NULL,
            title         VARCHAR(200) NOT NULL,
            description   TEXT NOT NULL,
            barangay      VARCHAR(100) NOT NULL,
            location      VARCHAR(255) NOT NULL,
            activity_type ENUM('cleanup_drive','environmental_education','tree_planting','other') NOT NULL,
            start_date    DATETIME NOT NULL,
            end_date      DATETIME,
            image_url     VARCHAR(255),
            status        ENUM('upcoming','ongoing','completed') DEFAULT 'upcoming',
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    print("[OK] Tables created")

    # 9. Seed admin user
    cursor.execute("SELECT id FROM users WHERE email='admin@ecotrack.com'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (name,email,password,role,points) VALUES (%s,%s,%s,'admin',%s)",
            ('Admin', 'admin@ecotrack.com', hash_pw('admin123'), 0)
        )
        print("[OK] Admin account created (admin@ecotrack.com / admin123)")
    else:
        print("[INFO] Admin account already exists")

    # 10. Seed demo user
    cursor.execute("SELECT id FROM users WHERE email='user@ecotrack.com'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (name,email,password,role,points) VALUES (%s,%s,%s,'user',%s)",
            ('Juan dela Cruz', 'user@ecotrack.com', hash_pw('user123'), 50)
        )
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email='user@ecotrack.com'")
        uid = cursor.fetchone()[0]

        # Seed sample reports
        samples = [
            (uid, 'Overflowing bin near market', 'The trash bin near the public market has been overflowing for 3 days.',
             'Asinan', 'Public Market, Main St.', 'Near the main entrance', 'overflowing_bin', 'pending', 0),
            (uid, 'Illegal dumping at riverbank', 'Large piles of construction waste illegally dumped near the river.',
             'Gordon Heights', 'Riverbank', 'Behind the residential area', 'illegal_dumping', 'in_progress', 0),
            (uid, 'Uncollected garbage on Rizal Ave', 'Garbage has not been collected for over a week on this street.',
             'Kalaklan', 'Rizal Avenue, Block 4', 'Corner intersection', 'uncollected_garbage', 'resolved', 20),
        ]
        cursor.executemany(
            "INSERT INTO reports (user_id,title,description,barangay,location,location_notes,issue_type,status,points_awarded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            samples
        )
        print("[OK] Demo user created (user@ecotrack.com / user123)")
        print("[OK] Sample reports seeded")
    else:
        print("[INFO] Demo user already exists")

    conn.commit()
    cursor.close()
    conn.close()

    print("-" * 40)
    print("SETUP COMPLETE!")
    print("Run the app with:  python app.py")
    print("Then open:         http://localhost:5000")

if __name__ == '__main__':
    run()

