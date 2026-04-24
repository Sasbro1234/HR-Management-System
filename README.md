# 🏢 HR Management System

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

A fully-featured, modern HR Management System built with Django. This system handles multiple HR aspects including employee records, attendance tracking, leave requests, and payroll distribution.

---

## ✨ Features

- **🧑‍💼 Built-in Roles & Authentication**
  - **HR Manager (Admin):** Full access to create employees, approve leaves, create payroll, and monitor attendance.
  - **Employee:** Can view their profile, request leaves, view their salary history, and clock in/out for attendance.
- **📁 Employee Management**
  - Comprehensive employee details including personal, role, department, and contact info.
- **⏰ Attendance Tracking**
  - Web-based clock-in/clock-out functionality for employees.
  - Timesheet logs accessible by HR.
- **🗓️ Leave Management**
  - Employees can request leaves with specific dates and reasons.
  - HR Manager can approve or reject leaves with status tracking.
- **💰 Payroll System**
  - Generates payroll/salary structures dynamically base on base salaries and deductions.

---

## 🚀 Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/Sasbro1234/HR-Management-System.git
   cd HR-Management-System
   ```

2. **Create a Virtual Environment** (Optional but Recommended - DO NOT push to Git):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**
   *(If db.sqlite3 is already present, you can skip this, but it's safe to run)*
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   > Visit `http://127.0.0.1:8000/` in your browser!

---

## 🔐 System Logins

A pre-populated sandbox database is included out of the box with the following accounts.

### 👑 Admin / HR Manager
Use this account to access the core Dashboard and Django Admin Panel.
- **Username:** `admin`
- **Password:** `admin123`

### 👔 Employee
Use this account to test the employee perspective (requesting leave, clock-in, etc).
- **Username:** `employee`
- **Password:** `employee123`

---

## 🛠️ Generating New Sandbox Users

If you want to reset or re-create default sandbox users from scratch, simply run:
```bash
python create_users.py
```
This script will construct the primary `admin` and `employee` entities automatically.

---
**Project Structure Notes:** 
Static files like CSS & images have been implemented directly within HTML via internal-styling for maximum portability without external caching dependencies. File uploads are stored strictly inside the local `/media/` folder.

## Admin Access
To create an admin account, run: `python manage.py createsuperuser`
Then access the admin panel at `http://127.0.0.1:8000/admin/`.
