# import os
# from datetime import datetime
# from bson import ObjectId
# from dotenv import load_dotenv


# from flask import (
#     Flask,
#     render_template,
#     request,
#     redirect,
#     url_for,
#     flash,
# )
# from flask_bcrypt import Bcrypt
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     login_required,
#     logout_user,
#     current_user,
# )
# from pymongo import MongoClient

# # Load environment variables
# load_dotenv()

# MONGODB_URI = os.getenv("MONGODB_URI", "")
# DB_NAME = os.getenv("MONGODB_DB_NAME", "tutoringdb")
# SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

# app = Flask(__name__)
# app.secret_key = SECRET_KEY


# # Database
# if not MONGODB_URI:
#     # Warn early in console to help users configure Atlas
#     print("[v0] Warning: MONGODB_URI is not set. Please configure it in .env")
# client = MongoClient(MONGODB_URI) if MONGODB_URI else None
# db = client[DB_NAME] if client is not None else None
# users_col = db["users"] if db is not None else None
# queries_col = db["queries"] if db is not None else None

# # Auth
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "warning"

# # Require authentication for all pages except login/register/static
# @app.before_request
# def require_login_for_site():
#     # Allow unauthenticated access only to login, register, and static files
#     allowed = {"login", "register", "static"}
#     if request.endpoint and request.endpoint in allowed:
#         return
#     if request.endpoint is None:
#         # Could be 404 or other; let Flask handle it
#         return
#     if not current_user.is_authenticated:
#         return redirect(url_for("login"))

# class User(UserMixin):
#     def __init__(self, doc):
#         self.doc = doc
#         self.id = str(doc["_id"])
#         self.name = doc.get("name")
#         self.email = doc.get("email")
#         self.year = doc.get("year")
#         self.subject = doc.get("subject")

#     @staticmethod
#     def find_by_id(user_id: str):
#         if users_col is None:
#             return None
#         try:
#             doc = users_col.find_one({"_id": ObjectId(user_id)})
#             return User(doc) if doc else None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_email(email: str):
#         if users_col is None:
#             return None
#         doc = users_col.find_one({"email": email.strip().lower()})
#         return User(doc) if doc else None


# @login_manager.user_loader
# def load_user(user_id):
#     return User.find_by_id(user_id)


# def validate_registration(form):
#     errors = []
#     name = form.get("name", "").strip()
#     email = form.get("email", "").strip().lower()
#     year = form.get("year", "").strip()
#     subject = form.get("subject", "").strip()
#     password = form.get("password", "")

#     if not name or len(name) < 2:
#         errors.append("Please enter your full name (min 2 characters).")
#     if not email or "@" not in email:
#         errors.append("Please provide a valid email address.")
#     if not year.isdigit() or not (1 <= int(year) <= 10):
#         errors.append("Year of study must be a number between 1 and 10.")
#     if not subject:
#         errors.append("Please choose a subject of interest.")
#     if not password or len(password) < 6:
#         errors.append("Password must be at least 6 characters.")
#     return errors


# def sample_timetable():
#     # Example static schedule; replace with real data as needed
#     return [
#         {"day": "Monday", "time": "5:00 PM - 6:00 PM", "topic": "Python Basics"},
#         {"day": "Wednesday", "time": "5:00 PM - 6:00 PM", "topic": "Operating Systems"},
#         {"day": "Friday", "time": "5:00 PM - 6:00 PM", "topic": "Computer Networks"},
#     ]


# @app.route("/")
# def home():
#     return render_template("home.html")


# @app.route("/about")
# def about():
#     # Render dedicated about page instead of home template section
#     return render_template("about.html")

# @app.route('/work')
# def work():
#     return render_template('work.html')


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         if users_col is None:
#             flash("Database is not configured. Please set MONGODB_URI.", "danger")
#             return redirect(url_for("register"))

#         errors = validate_registration(request.form)
#         if errors:
#             for e in errors:
#                 flash(e, "danger")
#             return render_template("register.html", form=request.form)

#         name = request.form.get("name").strip()
#         email = request.form.get("email").strip().lower()
#         year = int(request.form.get("year").strip())
#         subject = request.form.get("subject").strip()
#         password = request.form.get("password")

#         # unique email check
#         if users_col.find_one({"email": email}):
#             flash("An account with this email already exists.", "warning")
#             return render_template("register.html", form=request.form)

#         pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
#         user_doc = {
#             "name": name,
#             "email": email,
#             "year": year,
#             "subject": subject,
#             "passwordHash": pw_hash,
#             "createdAt": datetime.utcnow(),
#         }
#         result = users_col.insert_one(user_doc)
#         flash("Registration successful! Please log in.", "success")
#         return redirect(url_for("login"))
#     return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         if users_col is None:
#             flash("Database is not configured. Please set MONGODB_URI.", "danger")
#             return redirect(url_for("login"))

#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "")

#         found = users_col.find_one({"email": email})
#         if not found:
#             flash("Invalid email or password.", "danger")
#             return render_template("login.html", form=request.form)

#         if not bcrypt.check_password_hash(found.get("passwordHash", ""), password):
#             flash("Invalid email or password.", "danger")
#             return render_template("login.html", form=request.form)

#         user = User(found)
#         # 👇 Temporary session only
#         login_user(user, remember=False)

#         flash(f"Welcome back, {user.name}!", "success")
#         return redirect(url_for("dashboard"))
#     return render_template("login.html")



# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     flash("You have been logged out.", "info")
#     return redirect(url_for("home"))


# @app.route("/dashboard")
# @login_required
# def dashboard():
#     # Display registered course details and schedule
#     schedule = sample_timetable()
#     return render_template("dashboard.html", schedule=schedule)


# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         if queries_col is None:
#             flash("Database is not configured. Please set MONGODB_URI.", "danger")
#             return redirect(url_for("contact"))

#         name = request.form.get("name", "").strip()
#         email = request.form.get("email", "").strip().lower()
#         message = request.form.get("message", "").strip()

#         if not name or not email or not message:
#             flash("All fields are required.", "danger")
#             return render_template("contact.html", form=request.form)

#         queries_col.insert_one(
#             {
#                 "name": name,
#                 "email": email,
#                 "message": message,
#                 "createdAt": datetime.utcnow(),
#             }
#         )
#         flash("Your message has been sent. Thank you!", "success")
#         return redirect(url_for("contact"))
#     return render_template("contact.html")


# if __name__ == "__main__":
#     # Enable debug in development only
#     app.run(host="0.0.0.0", port=5000, debug=True)



import os
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("MONGODB_DB_NAME", "tutoringdb")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Database
if not MONGODB_URI:
    print("[v0] Warning: MONGODB_URI is not set. Please configure it in .env")

client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client[DB_NAME] if client is not None else None
users_col = db["users"] if db is not None else None
queries_col = db["queries"] if db is not None else None

# Auth
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

# Require authentication for all pages except login/register/static
@app.before_request
def require_login_for_site():
    allowed = {"login", "register", "static", "home", "about", "contact"}
    if request.endpoint and request.endpoint in allowed:
        return
    if request.endpoint is None:
        return
    if not current_user.is_authenticated:
        return redirect(url_for("login"))


class User(UserMixin):
    def __init__(self, doc):
        self.doc = doc
        self.id = str(doc["_id"])
        self.name = doc.get("name")
        self.email = doc.get("email")
        self.year = doc.get("year")
        self.subject = doc.get("subject")
        self.contact = doc.get("contact")  # ✅ added contact

    @staticmethod
    def find_by_id(user_id: str):
        if users_col is None:
            return None
        try:
            doc = users_col.find_one({"_id": ObjectId(user_id)})
            return User(doc) if doc else None
        except Exception:
            return None

    @staticmethod
    def find_by_email(email: str):
        if users_col is None:
            return None
        doc = users_col.find_one({"email": email.strip().lower()})
        return User(doc) if doc else None


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


# ✅ Updated to include contact validation
def validate_registration(form):
    errors = []
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    contact = form.get("contact", "").strip()
    year = form.get("year", "").strip()
    subject = form.get("subject", "").strip()
    password = form.get("password", "")

    if not name or len(name) < 2:
        errors.append("Please enter your full name (min 2 characters).")
    if not email or "@" not in email:
        errors.append("Please provide a valid email address.")
    if not contact.isdigit() or len(contact) != 10:
        errors.append("Please provide a valid 10-digit contact number.")
    if not year.isdigit() or not (1 <= int(year) <= 10):
        errors.append("Year of study must be a number between 1 and 10.")
    if not subject:
        errors.append("Please choose a subject of interest.")
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    return errors


def sample_timetable():
    return [
        {"day": "Monday", "time": "5:00 PM - 6:00 PM", "topic": "Python Basics"},
        {"day": "Wednesday", "time": "5:00 PM - 6:00 PM", "topic": "Operating Systems"},
        {"day": "Friday", "time": "5:00 PM - 6:00 PM", "topic": "Computer Networks"},
    ]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/work')
def work():
    return render_template('work.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if users_col is None:
            flash("Database is not configured. Please set MONGODB_URI.", "danger")
            return redirect(url_for("register"))

        errors = validate_registration(request.form)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("register.html", form=request.form)

        name = request.form.get("name").strip()
        email = request.form.get("email").strip().lower()
        contact = request.form.get("contact").strip()
        year = int(request.form.get("year").strip())
        subject = request.form.get("subject").strip()
        password = request.form.get("password")

        if users_col.find_one({"email": email}):
            flash("An account with this email already exists.", "warning")
            return render_template("register.html", form=request.form)

        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user_doc = {
            "name": name,
            "email": email,
            "contact": contact,  # ✅ added to DB
            "year": year,
            "subject": subject,
            "passwordHash": pw_hash,
            "createdAt": datetime.utcnow(),
        }
        users_col.insert_one(user_doc)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if users_col is None:
            flash("Database is not configured. Please set MONGODB_URI.", "danger")
            return redirect(url_for("login"))

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        found = users_col.find_one({"email": email})
        if not found or not bcrypt.check_password_hash(found.get("passwordHash", ""), password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html", form=request.form)

        user = User(found)
        login_user(user, remember=False)

        flash(f"Welcome back, {user.name}!", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    schedule = sample_timetable()
    return render_template("dashboard.html", schedule=schedule)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if queries_col is None:
            flash("Database is not configured. Please set MONGODB_URI.", "danger")
            return redirect(url_for("contact"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("All fields are required.", "danger")
            return render_template("contact.html", form=request.form)

        queries_col.insert_one(
            {
                "name": name,
                "email": email,
                "message": message,
                "createdAt": datetime.utcnow(),
            }
        )
        flash("Your message has been sent. Thank you!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
