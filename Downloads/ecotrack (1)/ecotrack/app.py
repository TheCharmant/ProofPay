from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from functools import wraps
import mysql.connector
import hashlib
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'ecotrack_secret_key_2024'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ecotrack_db'
}

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

BARANGAYS = [
    'Asinan','Banicain','Barretto','East Bajac-Bajac','East Tapinac',
    'Gordon Heights','Kalaklan','Mabayuan','New Cabalan','New Kababae',
    'New Kalalake','New Ilalim','Old Cabalan','Pag-Asa','Santa Rita',
    'West Bajac-Bajac','West Tapinac'
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_action(user_id, user_name, action):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO activity_log (user_id, user_name, action) VALUES (%s,%s,%s)",
            (user_id, user_name, action)
        )
        db.commit()
        cursor.close(); db.close()
    except:
        pass

def add_points(user_id, points, reason, given_by=None):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO points (user_id, points, reason, given_by) VALUES (%s,%s,%s,%s)",
            (user_id, points, reason, given_by)
        )
        cursor.execute(
            "UPDATE users SET total_points = total_points + %s WHERE id=%s",
            (points, user_id)
        )
        db.commit()
        cursor.close(); db.close()
    except:
        pass

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── INDEX ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('admin_dashboard') if session.get('role') == 'admin' else url_for('user_dashboard'))
    return render_template('landing.html')

# ── AUTH ──────────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].strip().lower()
        password = hash_password(request.form['password'])
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password, role, total_points) VALUES (%s,%s,%s,'user',0)",
                (name, email, password)
            )
            db.commit()
            cursor.close(); db.close()
            log_action(None, name, f'New user registered: {email}')
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already registered.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = hash_password(request.form['password'])
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE LOWER(email)=%s", (email,))
            user = cursor.fetchone()
            cursor.close(); db.close()
            if not user:
                flash('No account found with that email address.', 'error')
            elif user['password'] != password:
                flash('Incorrect password.', 'error')
            else:
                session['user_id'] = user['id']
                session['name'] = user['name']
                session['role'] = user['role']
                log_action(user['id'], user['name'], 'Logged in')
                return redirect(url_for('admin_dashboard') if user['role'] == 'admin' else url_for('user_dashboard'))
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_action(session.get('user_id'), session.get('name'), 'Logged out')
    session.clear()
    return redirect(url_for('index'))

# ── USER DASHBOARD ────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def user_dashboard():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reports WHERE user_id=%s ORDER BY created_at DESC", (session['user_id'],))
        reports = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) as total FROM reports WHERE user_id=%s", (session['user_id'],))
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='resolved'", (session['user_id'],))
        resolved = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='pending'", (session['user_id'],))
        pending = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='in_progress'", (session['user_id'],))
        in_progress = cursor.fetchone()['c']
        cursor.execute("SELECT total_points FROM users WHERE id=%s", (session['user_id'],))
        pts = cursor.fetchone()
        user_points = pts['total_points'] if pts else 0
        cursor.execute("SELECT * FROM announcements WHERE is_active=1 ORDER BY created_at DESC LIMIT 1")
        announcement = cursor.fetchone()
        cursor.close(); db.close()
        return render_template('user_dashboard.html', reports=reports,
                               total=total, resolved=resolved, pending=pending,
                               in_progress=in_progress, announcement=announcement,
                               user_points=user_points)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('user_dashboard.html', reports=[], total=0,
                               resolved=0, pending=0, in_progress=0,
                               announcement=None, user_points=0)

# ── NEW REPORT ────────────────────────────────────────────────────────────────
@app.route('/report/new', methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        barangay = request.form['barangay']
        street = request.form.get('street', '')
        location = f"{street}, {barangay}" if street else barangay
        issue_type = request.form['issue_type']
        image_path = None
        if 'image' in request.files:
            image_path = save_upload(request.files['image'])
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO reports (user_id,title,description,location,barangay,street,issue_type,status,image_path) VALUES (%s,%s,%s,%s,%s,%s,%s,'pending',%s)",
                (session['user_id'], title, description, location, barangay, street, issue_type, image_path)
            )
            db.commit()
            cursor.close(); db.close()
            add_points(session['user_id'], 5, 'Submitted a waste report')
            log_action(session['user_id'], session['name'], f'Submitted report: {title}')
            flash('Report submitted! You earned 5 points.', 'success')
            return redirect(url_for('user_dashboard'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    return render_template('new_report.html', barangays=BARANGAYS)

# ── VIEW REPORT ───────────────────────────────────────────────────────────────
@app.route('/report/<int:report_id>')
@login_required
def view_report(report_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name as reporter_name
            FROM reports r JOIN users u ON r.user_id=u.id WHERE r.id=%s
        """, (report_id,))
        report = cursor.fetchone()
        if not report:
            flash('Report not found.', 'error')
            return redirect(url_for('user_dashboard'))
        if session.get('role') != 'admin' and report['user_id'] != session['user_id']:
            flash('Access denied.', 'error')
            return redirect(url_for('user_dashboard'))
        cursor.execute("""
            SELECT c.*, u.name as commenter_name, u.role as commenter_role
            FROM comments c JOIN users u ON c.user_id=u.id
            WHERE c.report_id=%s ORDER BY c.created_at ASC
        """, (report_id,))
        comments = cursor.fetchall()
        cursor.execute("SELECT * FROM resolution_images WHERE report_id=%s ORDER BY created_at DESC", (report_id,))
        resolution_images = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('view_report.html', report=report,
                               comments=comments, resolution_images=resolution_images)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('user_dashboard'))

# ── UPLOAD RESOLUTION IMAGE ───────────────────────────────────────────────────
@app.route('/report/<int:report_id>/upload-resolution', methods=['POST'])
@admin_required
def upload_resolution(report_id):
    if 'image' not in request.files:
        flash('No image selected.', 'error')
        return redirect(url_for('view_report', report_id=report_id))
    image_path = save_upload(request.files['image'])
    if not image_path:
        flash('Invalid image format.', 'error')
        return redirect(url_for('view_report', report_id=report_id))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO resolution_images (report_id, image_path, uploaded_by) VALUES (%s,%s,%s)",
            (report_id, image_path, session['user_id'])
        )
        db.commit()
        cursor.close(); db.close()
        log_action(session['user_id'], session['name'], f'Uploaded resolution image for report #{report_id}')
        flash('Resolution image uploaded!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('view_report', report_id=report_id))

# ── COMMENT ───────────────────────────────────────────────────────────────────
@app.route('/report/<int:report_id>/comment', methods=['POST'])
@login_required
def add_comment(report_id):
    message = request.form.get('message', '').strip()
    if not message:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('view_report', report_id=report_id))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO comments (report_id, user_id, message) VALUES (%s,%s,%s)",
                       (report_id, session['user_id'], message))
        db.commit()
        cursor.close(); db.close()
        log_action(session['user_id'], session['name'], f'Commented on report #{report_id}')
        flash('Comment added!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('view_report', report_id=report_id))

# ── DELETE REPORT ─────────────────────────────────────────────────────────────
@app.route('/report/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reports WHERE id=%s", (report_id,))
        report = cursor.fetchone()
        if not report:
            flash('Report not found.', 'error')
        elif session.get('role') != 'admin' and report['user_id'] != session['user_id']:
            flash('Access denied.', 'error')
        else:
            cursor.execute("DELETE FROM reports WHERE id=%s", (report_id,))
            db.commit()
            log_action(session['user_id'], session['name'], f'Deleted report #{report_id}')
            flash('Report deleted.', 'success')
        cursor.close(); db.close()
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard') if session.get('role') == 'admin' else url_for('user_dashboard'))

# ── MY STATS ──────────────────────────────────────────────────────────────────
@app.route('/my-stats')
@login_required
def my_stats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT issue_type, COUNT(*) as count FROM reports WHERE user_id=%s GROUP BY issue_type", (session['user_id'],))
        by_type = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) as count FROM reports WHERE user_id=%s GROUP BY status", (session['user_id'],))
        by_status = cursor.fetchall()
        cursor.execute("""
            SELECT DATE_FORMAT(created_at,'%%Y-%%m') as month, COUNT(*) as count
            FROM reports WHERE user_id=%s GROUP BY month ORDER BY month ASC LIMIT 6
        """, (session['user_id'],))
        by_month = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s", (session['user_id'],))
        total = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='resolved'", (session['user_id'],))
        resolved = cursor.fetchone()['c']
        cursor.execute("SELECT total_points FROM users WHERE id=%s", (session['user_id'],))
        pts = cursor.fetchone()
        user_points = pts['total_points'] if pts else 0
        cursor.execute("SELECT * FROM points WHERE user_id=%s ORDER BY created_at DESC LIMIT 10", (session['user_id'],))
        point_history = cursor.fetchall()
        resolution_rate = round((resolved / total * 100) if total > 0 else 0)
        cursor.close(); db.close()
        return render_template('my_stats.html', by_type=by_type, by_status=by_status,
                               by_month=by_month, total=total, resolved=resolved,
                               resolution_rate=resolution_rate, user_points=user_points,
                               point_history=point_history)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('user_dashboard'))

# ── FEED (USER) ───────────────────────────────────────────────────────────────
@app.route('/feed')
@login_required
def feed():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, u.name as organizer,
            (SELECT COUNT(*) FROM activity_participants WHERE activity_id=a.id) as participant_count,
            (SELECT COUNT(*) FROM activity_participants WHERE activity_id=a.id AND user_id=%s) as joined
            FROM activities a JOIN users u ON a.created_by=u.id
            ORDER BY a.activity_date ASC
        """, (session['user_id'],))
        activities = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('feed.html', activities=activities)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('feed.html', activities=[])

# ── JOIN ACTIVITY ─────────────────────────────────────────────────────────────
@app.route('/activity/<int:activity_id>/join', methods=['POST'])
@login_required
def join_activity(activity_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM activity_participants WHERE activity_id=%s AND user_id=%s",
                       (activity_id, session['user_id']))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("DELETE FROM activity_participants WHERE activity_id=%s AND user_id=%s",
                           (activity_id, session['user_id']))
            db.commit()
            flash('You have left the activity.', 'success')
        else:
            cursor.execute("INSERT INTO activity_participants (activity_id, user_id) VALUES (%s,%s)",
                           (activity_id, session['user_id']))
            db.commit()
            log_action(session['user_id'], session['name'], f'Joined activity #{activity_id}')
            flash('You joined the activity!', 'success')
        cursor.close(); db.close()
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('feed'))

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'update_profile':
                name = request.form['name']
                bio = request.form.get('bio', '')
                cursor.execute("UPDATE users SET name=%s, bio=%s WHERE id=%s",
                               (name, bio, session['user_id']))
                db.commit()
                session['name'] = name
                flash('Profile updated!', 'success')
            elif action == 'change_password':
                current = hash_password(request.form['current_password'])
                new_pw = request.form['new_password']
                confirm = request.form['confirm_password']
                cursor.execute("SELECT password FROM users WHERE id=%s", (session['user_id'],))
                row = cursor.fetchone()
                if row['password'] != current:
                    flash('Current password is incorrect.', 'error')
                elif new_pw != confirm:
                    flash('New passwords do not match.', 'error')
                else:
                    cursor.execute("UPDATE users SET password=%s WHERE id=%s",
                                   (hash_password(new_pw), session['user_id']))
                    db.commit()
                    flash('Password updated!', 'success')
            cursor.close(); db.close()
            return redirect(url_for('profile'))
        cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s", (session['user_id'],))
        report_count = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='pending'", (session['user_id'],))
        pending_count = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE user_id=%s AND status='resolved'", (session['user_id'],))
        resolved_count = cursor.fetchone()['c']
        cursor.execute("SELECT * FROM points WHERE user_id=%s ORDER BY created_at DESC LIMIT 5", (session['user_id'],))
        recent_points = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('profile.html', user=user, report_count=report_count,
                               pending_count=pending_count, resolved_count=resolved_count,
                               recent_points=recent_points)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('user_dashboard'))

# ── ADMIN DASHBOARD ───────────────────────────────────────────────────────────
@app.route('/admin')
@admin_required
def admin_dashboard():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name as reporter_name
            FROM reports r JOIN users u ON r.user_id=u.id ORDER BY r.created_at DESC
        """)
        reports = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) as total FROM reports")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='pending'")
        pending = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='in_progress'")
        in_progress = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='resolved'")
        resolved = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM users WHERE role='user'")
        users_count = cursor.fetchone()['c']
        cursor.execute("SELECT * FROM announcements WHERE is_active=1 ORDER BY created_at DESC LIMIT 1")
        announcement = cursor.fetchone()
        cursor.close(); db.close()
        return render_template('admin_dashboard.html', reports=reports, total=total,
                               pending=pending, in_progress=in_progress, resolved=resolved,
                               users_count=users_count, announcement=announcement)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('admin_dashboard.html', reports=[], total=0,
                               pending=0, in_progress=0, resolved=0, users_count=0, announcement=None)

# ── UPDATE REPORT ─────────────────────────────────────────────────────────────
@app.route('/admin/report/<int:report_id>/update', methods=['POST'])
@admin_required
def update_report(report_id):
    status = request.form['status']
    admin_notes = request.form.get('admin_notes', '')
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE reports SET status=%s, admin_notes=%s, updated_at=NOW() WHERE id=%s",
                       (status, admin_notes, report_id))
        db.commit()
        cursor.close(); db.close()
        log_action(session['user_id'], session['name'], f'Updated report #{report_id} to {status}')
        flash('Report updated!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('view_report', report_id=report_id))

# ── ADMIN GIVE POINTS ─────────────────────────────────────────────────────────
@app.route('/admin/give-points', methods=['POST'])
@admin_required
def give_points():
    user_id = request.form['user_id']
    points = int(request.form['points'])
    reason = request.form['reason']
    add_points(user_id, points, reason, given_by=session['user_id'])
    log_action(session['user_id'], session['name'], f'Gave {points} points to user #{user_id}')
    flash(f'{points} points awarded!', 'success')
    return redirect(url_for('admin_users'))

# ── ADMIN USERS ───────────────────────────────────────────────────────────────
@app.route('/admin/users')
@admin_required
def admin_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, COUNT(r.id) as report_count
            FROM users u LEFT JOIN reports r ON u.id=r.user_id
            GROUP BY u.id ORDER BY u.total_points DESC
        """)
        users = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('admin_users.html', users=users)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('admin_users.html', users=[])

# ── ADMIN SEARCH ──────────────────────────────────────────────────────────────
@app.route('/admin/search')
@admin_required
def admin_search():
    query = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    itype = request.args.get('issue_type', '')
    barangay = request.args.get('barangay', '')
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        sql = "SELECT r.*, u.name as reporter_name FROM reports r JOIN users u ON r.user_id=u.id WHERE 1=1"
        params = []
        if query:
            sql += " AND (r.title LIKE %s OR r.description LIKE %s OR r.location LIKE %s OR u.name LIKE %s)"
            like = f'%{query}%'
            params += [like, like, like, like]
        if status:
            sql += " AND r.status=%s"; params.append(status)
        if itype:
            sql += " AND r.issue_type=%s"; params.append(itype)
        if barangay:
            sql += " AND r.barangay=%s"; params.append(barangay)
        sql += " ORDER BY r.created_at DESC"
        cursor.execute(sql, params)
        reports = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('admin_search.html', reports=reports,
                               query=query, status=status, issue_type=itype,
                               barangay=barangay, barangays=BARANGAYS)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

# ── ADMIN ACTIVITIES (FEED MANAGEMENT) ───────────────────────────────────────
@app.route('/admin/activities', methods=['GET', 'POST'])
@admin_required
def admin_activities():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'create':
                title = request.form['title']
                description = request.form['description']
                location = request.form['location']
                barangay = request.form['barangay']
                start_date = request.form['start_date']
                end_date = request.form.get('end_date', start_date)
                activity_type = request.form.get('activity_type', 'cleanup_drive')
                points_reward = int(request.form.get('points_reward', 10))
                image_url = None
                if 'image' in request.files:
                    image_url = save_uploaded_file(request.files['image'])
                cursor.execute("""
                    INSERT INTO activities (title,description,location,barangay,start_date,end_date,activity_type,admin_id,image_url,points_reward)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (title, description, location, barangay, start_date, end_date, activity_type,
                      session['user_id'], image_url, points_reward))
                db.commit()
                log_action(session['user_id'], session['name'], f'Created activity: {title}')
                flash('Activity posted!', 'success')
            elif action == 'update_status':
                act_id = request.form['activity_id']
                new_status = request.form['status']
                cursor.execute("UPDATE activities SET status=%s WHERE id=%s", (new_status, act_id))
                db.commit()
                flash('Activity status updated!', 'success')
            elif action == 'delete':
                act_id = request.form['activity_id']
                cursor.execute("DELETE FROM activities WHERE id=%s", (act_id,))
                db.commit()
                flash('Activity deleted.', 'success')
            elif action == 'award_points':
                act_id = request.form['activity_id']
                cursor.execute("""
                    SELECT ap.user_id, a.points_reward, a.title
                    FROM activity_participants ap JOIN activities a ON ap.activity_id=a.id
                    WHERE ap.activity_id=%s AND ap.status != 'completed'
                """, (act_id,))
                participants = cursor.fetchall()
                for p in participants:
                    add_points(p['user_id'], p['points_reward'],
                               f'Participated in: {p["title"]}', session['user_id'])
                cursor.execute("UPDATE activity_participants SET status='completed', points_awarded=%s WHERE activity_id=%s",
                               (participants[0]['points_reward'] if participants else 0, act_id))
                db.commit()
                flash(f'Points awarded to {len(participants)} participants!', 'success')
            cursor.close(); db.close()
            return redirect(url_for('admin_activities'))

        cursor.execute("""
            SELECT a.*, u.name as organizer,
            (SELECT COUNT(*) FROM activity_participants WHERE activity_id=a.id) as participant_count
            FROM activities a JOIN users u ON a.admin_id=u.id ORDER BY a.start_date DESC
        """)
        activities = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('admin_activities.html', activities=activities, barangays=BARANGAYS)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('admin_activities.html', activities=[], barangays=BARANGAYS)

# ── ACTIVITY PARTICIPANTS ─────────────────────────────────────────────────────
@app.route('/admin/activity/<int:activity_id>/participants')
@admin_required
def activity_participants(activity_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM activities WHERE id=%s", (activity_id,))
        activity = cursor.fetchone()
        cursor.execute("""
            SELECT u.name, u.email, u.total_points, ap.joined_at, ap.attended, ap.points_awarded
            FROM activity_participants ap JOIN users u ON ap.user_id=u.id
            WHERE ap.activity_id=%s ORDER BY ap.joined_at ASC
        """, (activity_id,))
        participants = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('activity_participants.html', activity=activity, participants=participants)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_activities'))

# ── REPORT GENERATION ─────────────────────────────────────────────────────────
@app.route('/admin/reports/generate')
@admin_required
def generate_report():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM reports")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='pending'")
        pending = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='in_progress'")
        in_progress = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM reports WHERE status='resolved'")
        resolved = cursor.fetchone()['c']
        cursor.execute("SELECT barangay, COUNT(*) as count FROM reports WHERE barangay IS NOT NULL GROUP BY barangay ORDER BY count DESC")
        by_barangay = cursor.fetchall()
        cursor.execute("SELECT issue_type, COUNT(*) as count FROM reports GROUP BY issue_type ORDER BY count DESC")
        by_type = cursor.fetchall()
        cursor.execute("""
            SELECT u.name, u.email, u.total_points, COUNT(r.id) as report_count
            FROM users u LEFT JOIN reports r ON u.id=r.user_id
            WHERE u.role='user' GROUP BY u.id ORDER BY u.total_points DESC LIMIT 10
        """)
        top_users = cursor.fetchall()
        cursor.execute("""
            SELECT a.title, a.activity_date, a.barangay, a.status,
            (SELECT COUNT(*) FROM activity_participants WHERE activity_id=a.id) as participant_count
            FROM activities a ORDER BY a.activity_date DESC LIMIT 10
        """)
        recent_activities = cursor.fetchall()
        cursor.execute("""
            SELECT r.*, u.name as reporter_name
            FROM reports r JOIN users u ON r.user_id=u.id
            ORDER BY r.created_at DESC LIMIT 20
        """)
        recent_reports = cursor.fetchall()
        generated_at = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        cursor.close(); db.close()
        return render_template('admin_report.html',
                               total=total, pending=pending, in_progress=in_progress, resolved=resolved,
                               by_barangay=by_barangay, by_type=by_type, top_users=top_users,
                               recent_activities=recent_activities, recent_reports=recent_reports,
                               generated_at=generated_at)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

# ── ANNOUNCEMENTS ─────────────────────────────────────────────────────────────
@app.route('/admin/announcements', methods=['GET', 'POST'])
@admin_required
def admin_announcements():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'create':
                title = request.form['title']
                message = request.form['message']
                cursor.execute("INSERT INTO announcements (title,message,created_by) VALUES (%s,%s,%s)",
                               (title, message, session['user_id']))
                db.commit()
                flash('Announcement posted!', 'success')
            elif action == 'toggle':
                cursor.execute("UPDATE announcements SET is_active=NOT is_active WHERE id=%s",
                               (request.form['ann_id'],))
                db.commit()
                flash('Announcement updated!', 'success')
            elif action == 'delete':
                cursor.execute("DELETE FROM announcements WHERE id=%s", (request.form['ann_id'],))
                db.commit()
                flash('Announcement deleted!', 'success')
            cursor.close(); db.close()
            return redirect(url_for('admin_announcements'))
        cursor.execute("""
            SELECT a.*, u.name as author FROM announcements a
            JOIN users u ON a.created_by=u.id ORDER BY a.created_at DESC
        """)
        announcements = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('admin_announcements.html', announcements=announcements)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('admin_announcements.html', announcements=[])

# ── ACTIVITY LOG ──────────────────────────────────────────────────────────────
@app.route('/admin/activity-log')
@admin_required
def admin_activity():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM activity_log ORDER BY created_at DESC LIMIT 100")
        logs = cursor.fetchall()
        cursor.close(); db.close()
        return render_template('admin_activity.html', logs=logs)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('admin_activity.html', logs=[])

# ── API STATS ─────────────────────────────────────────────────────────────────
@app.route('/api/stats')
@admin_required
def api_stats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT issue_type, COUNT(*) as count FROM reports GROUP BY issue_type")
        by_type = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) as count FROM reports GROUP BY status")
        by_status = cursor.fetchall()
        cursor.close(); db.close()
        return jsonify({'by_type': by_type, 'by_status': by_status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)