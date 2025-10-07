# Tutoring Platform (Flask + MongoDB)

A simple tutoring platform built with Flask, Jinja templates, Bootstrap, and MongoDB Atlas.

## Features
- Home page with hero, tutor info, and WhatsApp QR image
- Register (Full Name, Email, Year of Study, Subject, Password)
- Login (email + password) with secure bcrypt hashing
- Dashboard with welcome message, registered course details, and sample timetable
- Contact form that saves messages to MongoDB
- Flash messages for success/error, responsive Bootstrap UI
- Deployment-ready structure (`app.py` entry point)

## Quickstart

1) Create and activate a virtual environment:
- macOS/Linux:
  python3 -m venv .venv
  source .venv/bin/activate
- Windows (PowerShell):
  py -3 -m venv .venv
  .venv\\Scripts\\Activate.ps1

2) Install dependencies:
  pip install -r requirements.txt

3) Configure environment variables:
- Copy .env.example to .env and set:
  MONGODB_URI="mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/tutoringdb?retryWrites=true&w=majority"
  MONGODB_DB_NAME="tutoringdb"   # optional
  SECRET_KEY="a-very-long-random-string"

4) Run the server:
- macOS/Linux:
  export FLASK_APP=app.py
  flask run --debug
- Windows (PowerShell):
  $env:FLASK_APP="app.py"
  flask run --debug

Visit http://localhost:5000

## WhatsApp QR
Replace the placeholder image at static/img/whatsapp-qr.jpg with your real WhatsApp QR code. You can also add a direct link button to https://wa.me/<your-number> inside templates/home.html.

## MongoDB Collections
- users: { name, email, year, subject, passwordHash, createdAt }
- queries: { name, email, message, createdAt }

## Notes
- Passwords are hashed using bcrypt (Flask-Bcrypt).
- Sessions and user login are managed by Flask-Login.
- Server-side validation is implemented; client-side uses native HTML5 + Bootstrap validation states.
