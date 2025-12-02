🎓 Student–Faculty Feedback Management System

A web-based system built using Flask, SQLite, HTML/CSS, and Python to collect and manage student feedback about faculty members at GIET University.
Students can submit feedback and suggestions, while faculty members can securely log in to view only their specific reviews.




🚀 Features
👨‍🎓 Student Side

  Login using Roll Number (e.g., 24cse014)

  Fill personal details

  Select a faculty member

  Submit detailed review & suggestions

  Receive confirmation via a Thank You page

👨‍🏫 Faculty Side

  Login using official GIET email

     Example: faculty1@giet.edu

  Password follows auto-generated pattern:

     facultyID@123  
     Ex: faculty1@giet.edu → faculty1@123


Dashboard displays only reviews meant for that specific faculty

Secure session-based access




🗄️ Backend Features

SQLite database for storing:

   Student information

   Faculty review data

Auto-creation of necessary tables on first run

Secure session management

Dynamic filtering: each faculty sees only their own feedback




🛠️ Tech Stack

Component 	          Technology
Backend	              Flask (Python)
Database	            SQLite
Frontend	            HTML, CSS
Hosting (optional)	  PythonAnywhere / Render



suggestion-box/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── student_login.html
│   ├── studentinfo.html
│   ├── review.html
│   ├── thankyou.html
│   ├── faculty_login.html
│   └── faculty_review.html
│
├── app.py
└── database.db (auto-created on first run)




🧩 How the System Works
1️⃣ Student Workflow

Student logs in using Roll Number

Student enters personal details

Student selects a faculty email (e.g., faculty1@giet.edu)

Feedback is stored in DB with:

  Student name

  Department

  Suggestion

  Faculty email (for mapping)

2️⃣ Faculty Workflow

Faculty logs in with GIET email

Password matches pattern:

     <facultyID>@123


System fetches all reviews linked to their email

Faculty sees only their reviews in the dashboard




🖥️ Installation & Setup
🔹 Step 1 — Clone the repository
                     git clone https://github.com/your_username/suggestion-box.git
                     cd suggestion-box

🔹 Step 2 — Install dependencies
                     pip install flask

🔹 Step 3 — Run the application
                     python app.py

🔹 Step 4 — Open in browser
                    http://127.0.0.1:5000/


  🔒 Default Faculty Logins
Email                       	Password
 faculty1@giet.edu            faculty1@123
faculty2@giet.edu             faculty2@123
faculty3@giet.edu             faculty3@123



📜 License

This project is for educational purposes under GIET University.
