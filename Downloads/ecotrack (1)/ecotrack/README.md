# 🌿 EcoTrack — Community Waste Reporting System
**CSC 221 - Application Development and Emerging Technologies**  
*Project by: Beltran, Phenylope Vianca C.*

---

## Prerequisites
- Python 3.9+
- XAMPP (MySQL + Apache)

---

## Setup Instructions

### Step 1 — Start XAMPP
Open XAMPP Control Panel and **Start** both **Apache** and **MySQL**.

### Step 2 — Create the Database
**Option A — Automatic (recommended):**
```bash
python init_db.py
```

**Option B — Manual via phpMyAdmin:**
1. Open `http://localhost/phpmyadmin`
2. Click **SQL** tab, paste contents of `database.sql`, click **Go**

### Step 3 — Install Python Dependencies
Open a terminal in this project folder and run:
```bash
pip install -r requirements.txt
```

### Step 4 — Run the App
```bash
python app.py
```

Then open: **http://localhost:5000**

---

## Demo Accounts

| Role  | Email                  | Password  |
|-------|------------------------|-----------|
| Admin | admin@ecotrack.com     | admin123  |
| User  | user@ecotrack.com      | user123   |

---

## Features

- ✅ User registration & login
- ✅ Submit waste reports (uncollected garbage, illegal dumping, overflowing bins, littering)
- ✅ Admin dashboard with Chart.js graphs (status + issue type)
- ✅ Report status tracking (Pending → In Progress → Resolved)
- ✅ Admin notes on reports
- ✅ Admin search & filter reports (keyword, status, issue type)
- ✅ User management page
- ✅ User profile editing (name, bio, change password)
- ✅ Delete reports (by owner or admin)
- ✅ Custom 404 page
- ✅ Auto database initializer (`init_db.py`)
- ✅ Responsive design (mobile & desktop)

## SDGs Supported
- 🏙️ SDG 11 — Sustainable Cities and Communities
- ♻️ SDG 12 — Responsible Consumption and Production
- 🌱 SDG 13 — Climate Action

## Tech Stack
| Layer     | Technology           |
|-----------|----------------------|
| Frontend  | HTML, CSS, JavaScript |
| Backend   | Python (Flask)       |
| Database  | MySQL                |
| Server    | XAMPP                |
