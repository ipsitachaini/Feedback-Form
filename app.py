from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"


# ===========================
# DATABASE INITIALIZATION
# ===========================
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # faculty table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )
    """)

    # reviews table (with faculty_email column)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            suggestion TEXT,
            faculty_email TEXT
        )
    """)

    conn.commit()
    conn.close()


# Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ===========================
# HOME → STUDENT LOGIN
# ===========================
@app.route("/")
def home():
    return render_template("student_login.html")


# ===========================
# STUDENT LOGIN USING ROLL NUMBER
# ===========================
@app.route("/student_login", methods=["POST"])
def student_login():
    roll = request.form["roll"]
    password = request.form["password"]

    # Allow any roll number like 24cse014
    if len(roll) >= 5:
        session["student_id"] = roll
        return redirect("/studentinfo")

    return "Invalid Roll Number. Please enter a valid roll like 24cse014."


# ===========================
# STUDENT INFO PAGE
# ===========================
@app.route("/studentinfo")
def studentinfo():
    if "student_id" not in session:
        return redirect("/")
    return render_template("studentinfo.html")


# ===========================
# SAVE STUDENT INFO → GO TO REVIEW PAGE
# ===========================
@app.route("/save_studentinfo", methods=["POST"])
def save_studentinfo():

    session["student_name"] = request.form["name"]
    session["semester"] = request.form["semester"]
    session["department"] = request.form["department"]
    session["roll"] = request.form["roll"]

    return redirect("/review")


# ===========================
# REVIEW PAGE
# ===========================
@app.route("/review")
def review_page():
    if "student_id" not in session:
        return redirect("/")
    return render_template("review.html")


# ===========================
# SUBMIT REVIEW → SAVE TO DB → THANK YOU
# ===========================
@app.route("/submit_review", methods=["POST"])
def submit_review():
    if "student_id" not in session:
        return redirect("/")

    name = session["student_name"]
    department = session["department"]

    faculty_email = request.form["faculty"]   # selected in review form
    suggestion = request.form["suggestion"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO reviews (name, department, suggestion, faculty_email) VALUES (?, ?, ?, ?)",
        (name, department, suggestion, faculty_email)
    )

    conn.commit()
    return render_template("thankyou.html")


# ===========================
# FACULTY LOGIN PAGE
# ===========================
@app.route("/faculty")
def faculty_page():
    return render_template("faculty_login.html")


# ===========================
# FACULTY LOGIN
# ===========================
# @app.route("/faculty_login", methods=["POST"])
# def faculty_login():
#     email = request.form["email"]
#     password = request.form["password"]

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM faculty WHERE email=? AND password=?", (email, password))
#     user = cur.fetchone()

#     if user:
#         session["faculty"] = True
#         session["faculty_email"] = email
#         return redirect("/faculty_review")

#     return "Invalid faculty login"


@app.route("/faculty_login", methods=["POST"])
def faculty_login():
    email = request.form["email"]
    password = request.form["password"]

    # 1. Check domain rule
    if not email.endswith("@giet.edu"):
        return "Invalid email. Please use your official @giet.edu faculty email."

    # 2. Extract the faculty ID from email
    faculty_id = email.split("@")[0]   # faculty1, faculty2, csehod

    # 3. Apply Pattern A → password = facultyID + "@123"
    expected_password = faculty_id + "@123"

    # 4. Validate password
    if password != expected_password:
        return "Invalid password for this faculty email."

    # 5. Successful login
    session["faculty"] = True
    session["faculty_email"] = email
    return redirect("/faculty_review")




# ===========================
# FACULTY REVIEW DASHBOARD
# ===========================
@app.route("/faculty_review")
def faculty_review():
    if "faculty" not in session:
        return redirect("/faculty")

    faculty_email = session["faculty_email"]

    conn = get_db()
    cur = conn.cursor()

    # Load reviews for THAT specific faculty only
    cur.execute("SELECT * FROM reviews WHERE faculty_email=? ORDER BY id DESC",
                (faculty_email,))
    data = cur.fetchall()

    return render_template("faculty_review.html", reviews=data)


# ===========================
# LOGOUT
# ===========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===========================
# MAIN
# ===========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
