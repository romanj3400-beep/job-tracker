import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

CORS(
    app,
    supports_credentials=True,
    origins=["http://127.0.0.1:5500"]
)
# MySQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
    "Application",
    backref="user",
    lazy=True
)

def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return db.session.get(User, user_id)

# Application model
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False)
    date_applied = db.Column(db.Date)
    follow_up_date = db.Column(db.Date)
    salary = db.Column(db.Integer)
    job_url = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "position": self.position,
            "location": self.location,
            "status": self.status,
            "date_applied": (
                self.date_applied.isoformat()
                if self.date_applied
                else None
            ),
	    "follow_up_date": (
  	     self.follow_up_date.isoformat()
             if self.follow_up_date
             else None
            ),
            "salary": self.salary,
            "job_url": self.job_url,
            "notes": self.notes,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }

    @app.route("/api/register", methods=["POST"])
    def register():
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({
                "error": "Username, email, and password are required"
            }), 400

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            return jsonify({
                "error": "Username or email already exists"
            }), 409

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user.id
        }), 201
    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "error": "Username and password are required"
            }), 400

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        if not check_password_hash(user.password_hash, password):
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        session["user_id"] = user.id
        session["username"] = user.username

        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        }), 200
    
    @app.route("/api/me", methods=["GET"])
    def get_current_user_info():
        user = get_current_user()

        if not user:
            return jsonify({
                "error": "Not logged in"
            }), 401

        return jsonify({
            "user_id": user.id,
            "username": user.username
        }), 200
    @app.route("/api/logout", methods=["POST"])
    def logout():
        session.clear()

        return jsonify({
            "message": "Logged out successfully"
        }), 200


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "JPbTrack API is running!"
    })


# GET all applications
@app.route("/api/applications", methods=["GET"])
def get_applications():
    user = get_current_user()

    if not user:
        return jsonify({
            "error": "You must be logged in"
        }), 401

    applications = Application.query.filter_by(
        user_id=user.id
    ).all()

    return jsonify([
        application.to_dict()
        for application in applications
    ])


# GET one application
@app.route("/api/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    user = get_current_user()

    if not user:
        return jsonify({
            "error": "You must be logged in"
        }), 401

    application = Application.query.filter_by(
            id=application_id,
            user_id=user.id
        ).first()

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404
    

    if application.user_id != user.id:
        return jsonify({
            "error": "You are not the owner of this application"
        }), 403

    return jsonify(application.to_dict())


# POST a new application
@app.route("/api/applications", methods=["POST"])
def create_application():
    user = get_current_user()

    if not user:
        return jsonify({
            "error": "You must be logged in"
        }), 401

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    required_fields = ["company", "position", "location"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    application = Application(
        company=data["company"],
        position=data["position"],
        location=data["location"],
        status=data.get("status", "Applied"),
        date_applied=(
            datetime.strptime(data["date_applied"], "%Y-%m-%d").date()
            if data.get("date_applied")
            else None
        ),
	follow_up_date=(
        datetime.strptime(data["follow_up_date"], "%Y-%m-%d").date()
        if data.get("follow_up_date")
        else None
	),
        salary=data.get("salary"),
        job_url=data.get("job_url"),
        notes=data.get("notes")
    )

    db.session.add(application)
    db.session.commit()

    return jsonify(application.to_dict()), 201


# DELETE an application
@app.route("/api/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):
    user = get_current_user()

    if not user:
        return jsonify({
            "error": "You must be logged in"
        }), 401

    application = Application.query.filter_by(
            id=application_id,
            user_id=user.id
        ).first()

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    if application.user_id != user.id:
        return jsonify({
            "error": "You are not the owner of this application"
        }), 403

    db.session.delete(application)
    db.session.commit()

    return jsonify({
        "message": "Application deleted successfully"
    })
@app.route("/api/applications/<int:id>", methods=["PUT"])
def update_application(id):
    user = get_current_user()

    if not user:
        return jsonify({
            "error": "You must be logged in"
        }), 401

    application = Application.query.filter_by(
            id=id,
            user_id=user.id
        ).first()

    if not application:
        return jsonify({"error": "Application not found"}), 404

    data = request.get_json()

    if "company" in data:
        application.company = data["company"]

    if "position" in data:
        application.position = data["position"]

    if "location" in data:
        application.location = data["location"]

    if "status" in data:
        application.status = data["status"]

    if "date_applied" in data:
        application.date_applied = (
            datetime.strptime(data["date_applied"], "%Y-%m-%d").date()
            if data["date_applied"]
            else None
        )

    if "follow_up_date" in data:
        application.follow_up_date = (
            datetime.strptime(data["follow_up_date"], "%Y-%m-%d").date()
            if data["follow_up_date"]
            else None
        )

    if "job_url" in data:
        application.job_url = data["job_url"]

    if "notes" in data:
        application.notes = data["notes"]

    if "salary" in data:
        application.salary = data["salary"]

    db.session.commit()

    return jsonify({
        "id": application.id,
        "company": application.company,
        "position": application.position,
        "location": application.location,
        "status": application.status,
        "date_applied": (
            application.date_applied.isoformat()
            if application.date_applied
            else None
        ),
        "follow_up_date": (
            application.follow_up_date.isoformat()
            if application.follow_up_date
            else None
        ),
        "job_url": application.job_url,
        "notes": application.notes,
        "salary": application.salary,
        "created_at": (
            application.created_at.isoformat()
            if application.created_at
            else None
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
