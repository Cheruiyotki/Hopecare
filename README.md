# HopeCare - Cancer Treatment & Screening Website

A web-based healthcare management system for cancer treatment and screening, built with Flask and MySQL.

## Features

### User Roles
- **Patient**: Access personal dashboard, view appointments, upload medical reports
- **Doctor**: Manage patients, view appointments, update diagnoses
- **Admin**: Manage users, view complaints, access all features

### Core Functionality
- User authentication (login/signup)
- Patient management
- Doctor dashboard with patient overview
- Appointment scheduling and viewing
- Medical report uploads
- Diagnosis management
- User administration (admin only)
- Complaint handling

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5

## Prerequisites

- Python 3.x
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   cd Hopecare
   ```

2. **Install dependencies**
   ```bash
   pip install flask pymysql
   ```

3. **Set up the database**
   - Create a MySQL database named `hopecare`
   - Create the required tables (users, patients, appointments, etc.)

4. **Configure database connection**
   Edit `app.py` with your MySQL credentials:
   ```python
   conn = pymysql.connect(
       host='localhost',
       user='your_username',
       password='your_password',
       db='hopecare'
   )
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
Hopecare/
├── app.py                 # Main Flask application
├── static/
│   ├── home.css          # Home page styles
│   ├── login.css         # Login page styles
│   ├── patient.css       # Patient dashboard styles
│   ├── patient.js        # Patient page JavaScript
│   └── images/           # Static images
└── templates/
    ├── home.html         # Landing page
    ├── login.html        # Login page
    ├── signup.html       # Signup page
    ├── patient.html      # Patient dashboard
    ├── doctor_dashboard.html
    ├── admin_dashboard.html
    ├── view_patients.html
    ├── view_appointments.html
    ├── manage_users.html
    ├── patient_history.html
    ├── update_patient.html
    ├── upload_report.html
    └── ...
```

## Database Schema

### Users Table
- id (INT, PRIMARY KEY)
- username (VARCHAR)
- password (VARCHAR)
- user_type (ENUM: 'patient', 'doctor', 'admin')

### Patients Table
- id (INT, PRIMARY KEY)
- name (VARCHAR)
- age (INT)
- diagnosis (TEXT)
- medical_report (VARCHAR)

### Appointments Table
- id (INT, PRIMARY KEY)
- patient_id (INT, FOREIGN KEY)
- doctor_id (INT, FOREIGN KEY)
- appointment_date (DATE)
- appointment_time (TIME)

## Usage

1. **Register** a new account (patient, doctor, or admin)
2. **Login** with your credentials
3. **Patients**: Upload reports, view appointments
4. **Doctors**: View patients, update diagnoses, manage appointments
5. **Admins**: Manage all users, view complaints

## Security Notes

- This is a basic implementation for demonstration purposes
- In production, use proper password hashing (e.g., bcrypt)
- Implement input validation and sanitization
- Use environment variables for sensitive data

## License

This project is for educational purposes.