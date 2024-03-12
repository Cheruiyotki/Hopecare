from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql

app = Flask(__name__)
app.secret_key = 'utf8mb4'

# MySQL connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='hopecare'
)

def execute_query(query, params=None):
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        return cur
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
    finally:
        cur.close()

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        params = (username, password)
        cur = execute_query(query, params)
        if cur:  # Check if cur is not None
            user = cur.fetchone()
            if user:
                session['user_id'] = user[0]
                session['user_type'] = user[3]
                if user[3] == 'patient':
                    return redirect(url_for('patient_dashboard'))
                elif user[3] == 'doctor':
                    return redirect(url_for('doctor_dashboard'))
                elif user[3] == 'admin':
                    return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('An error occurred while executing the query', 'error')
    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
        params = (username, password, user_type)
        execute_query(query, params)
        flash('Sign up successful!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route for the patient dashboard
@app.route('/patient-dashboard')
def patient_dashboard():
    if 'user_id' in session and session['user_type'] == 'patient':
        return render_template('patient.html')
    else:
        return redirect(url_for('login'))

# Route for the doctor dashboard
@app.route('/doctor-dashboard')
def doctor_dashboard():
    if 'user_id' in session and session['user_type'] == 'doctor':
        # Fetch the doctor's name from the database based on the user_id
        query = "SELECT username FROM users WHERE id = %s AND user_type = 'doctor'"
        params = (session['user_id'],)
        cur = execute_query(query, params)
        if cur:
            doctor = cur.fetchone()[0]
            session['doctor'] = doctor
            return render_template('doctor_dashboard.html')
        else:
            flash('Error fetching doctor information', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Route for viewing patients
@app.route('/view_patients')
def view_patients():
    if 'user_id' in session:
        # Fetch patient data from the database
        query = "SELECT * FROM patients"
        cur = execute_query(query)
        if cur:
            patients = cur.fetchall()
            return render_template('view_patients.html', patients=patients)
        else:
            flash('Error fetching patient data', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Route for viewing appointments
@app.route('/view_appointments')
def view_appointments():
    if 'user_id' in session:
        doctor_id = session['user_id']  # Assuming the user_id in the session is the doctor's id
        query = "SELECT a.id, p.name AS patient_name, a.appointment_date, a.appointment_time " \
                "FROM appointments a " \
                "JOIN patients p ON a.patient_id = p.id " \
                "WHERE a.doctor_id = %s"
        params = (doctor_id,)
        cur = execute_query(query, params)
        if cur:
            appointments = cur.fetchall()
            return render_template('view_appointments.html', appointments=appointments)
        else:
            flash('Error fetching appointment data', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# Route for updating patient diagnosis
@app.route('/patient/<int:patient_id>/diagnosis', methods=['GET', 'POST'])
def update_diagnosis(patient_id):
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        # Update diagnosis in the database
        query = "UPDATE patients SET diagnosis = %s WHERE id = %s"
        params = (diagnosis, patient_id)
        execute_query(query, params)
        flash('Diagnosis updated successfully', 'success')
        return redirect(url_for('view_patients'))
    else:
        # Fetch the patient's current diagnosis from the database
        query = "SELECT diagnosis FROM patients WHERE id = %s"
        params = (patient_id,)
        cur = execute_query(query, params)
        if cur:
            diagnosis = cur.fetchone()[0]
            return render_template('update_diagnosis.html', patient_id=patient_id, diagnosis=diagnosis)
        else:
            flash('Error fetching patient diagnosis', 'error')
            return redirect(url_for('view_patients'))

# Route for the admin dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' in session and session['user_type'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

# Route for managing users
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' in session and session['user_type'] == 'admin':
        if request.method == 'POST':
            action = request.form['action']
            if action == 'add':
                # Add a new user
                username = request.form['username']
                password = request.form['password']
                user_type = request.form['user_type']
                query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
                params = (username, password, user_type)
                execute_query(query, params)
                flash('User added successfully', 'success')
            elif action == 'update':
                # Update an existing user
                user_id = request.form['user_id']
                username = request.form['username']
                password = request.form['password']
                user_type = request.form['user_type']
                query = "UPDATE users SET username = %s, password = %s, user_type = %s WHERE id = %s"
                params = (username, password, user_type, user_id)
                execute_query(query, params)
                flash('User updated successfully', 'success')
            elif action == 'delete':
                # Delete a user
                user_id = request.form['user_id']
                query = "DELETE FROM users WHERE id = %s"
                params = (user_id,)
                execute_query(query, params)
                flash('User deleted successfully', 'success')

        users = fetch_users_from_database()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for('login'))

def fetch_users_from_database():
    query = "SELECT id, username, user_type FROM users"
    cur = execute_query(query)
    if cur:
        users = cur.fetchall()
        return users
    else:
        return []

# # Route for viewing appointments
# @app.route('/view_appointments')
# def view_appointments():
#     if 'user_id' in session:
#         if session['user_type'] == 'admin':
#             appointments = fetch_appointments_from_database()
#             return render_template('view_appointments.html', appointments=appointments)
#         else:
#             doctor_id = session['user_id']  # Assuming the user_id in the session is the doctor's id
#             query = "SELECT a.id, p.name AS patient_name, a.appointment_date, a.appointment_time " \
#                     "FROM appointments a " \
#                     "JOIN patients p ON a.patient_id = p.id " \
#                     "WHERE a.doctor_id = %s"
#             params = (doctor_id,)
#             cur = execute_query(query, params)
#             if cur:
#                 appointments = cur.fetchall()
#                 return render_template('view_appointments.html', appointments=appointments)
#             else:
#                 flash('Error fetching appointment data', 'error')
#                 return redirect(url_for('login'))
#     else:
#         return redirect(url_for('login'))

# def fetch_appointments_from_database():
#     query = "SELECT a.id, p.name AS patient_name, d.username AS doctor_name, a.appointment_date, a.appointment_time " \
#             "FROM appointments a " \
#             "JOIN patients p ON a.patient_id = p.id " \
#             "JOIN users d ON a.doctor_id = d.id"
#     cur = execute_query(query)
#     if cur:
#         appointments = cur.fetchall()
#         return appointments
#     else:
#         return []

# Route for viewing the admin's profile
@app.route('/view_profile')
def view_profile():
    if 'user_id' in session and session['user_type'] == 'admin':
        admin_profile = fetch_admin_profile_from_database(session['user_id'])
        if admin_profile:
            return render_template('view_profile.html', profile=admin_profile)
        else:
            flash('Error fetching admin profile', 'error')
            return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

def fetch_admin_profile_from_database(user_id):
    query = "SELECT username, user_type FROM users WHERE id = %s"
    params = (user_id,)
    cur = execute_query(query, params)
    if cur:
        profile = cur.fetchone()
        return profile
    else:
        return None

# Route for editing the admin's profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session and session['user_type'] == 'admin':
        if request.method == 'POST':
            # Handle form submission for updating the admin's profile
            username = request.form['username']
            password = request.form['password']
            query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
            params = (username, password, session['user_id'])
            execute_query(query, params)
            flash('Profile updated successfully', 'success')
            return redirect(url_for('view_profile'))
        admin_profile = fetch_admin_profile_from_database(session['user_id'])
        if admin_profile:
            return render_template('edit_profile.html', profile=admin_profile)
        else:
            flash('Error fetching admin profile', 'error')
            return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

# Route for viewing complaints
@app.route('/view_complaints')
def view_complaints():
    if 'user_id' in session and session['user_type'] == 'admin':
        complaints = fetch_complaints_from_database()
        return render_template('view_complaints.html', complaints=complaints)
    else:
        return redirect(url_for('login'))

def fetch_complaints_from_database():
    query = "SELECT c.id, p.name AS patient_name, c.complaint_description, c.complaint_date, c.status " \
            "FROM complaints c " \
            "JOIN patients p ON c.patient_id = p.id"
    cur = execute_query(query)
    if cur:   
        complaints = cur.fetchall()
        return complaints
    else:
        return []

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.pop('doctor', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)