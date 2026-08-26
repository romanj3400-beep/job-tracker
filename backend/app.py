import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# MySQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Application model
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False)
    date_applied = db.Column(db.Date)
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
            "salary": self.salary,
            "job_url": self.job_url,
            "notes": self.notes,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "JPbTrack API is running!"
    })


# GET all applications
@app.route("/api/applications", methods=["GET"])
def get_applications():
    applications = Application.query.all()

    return jsonify([
        application.to_dict()
        for application in applications
    ])


# GET one application
@app.route("/api/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    application = db.session.get(Application, application_id)

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    return jsonify(application.to_dict())


# POST a new application
@app.route("/api/applications", methods=["POST"])
def create_application():
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
    application = db.session.get(Application, application_id)

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    db.session.delete(application)
    db.session.commit()

    return jsonify({
        "message": "Application deleted successfully"
    })

@app.route("/api/applications/<int:id>", methods=["PUT"])
def update_application(id):
    application = Application.query.get(id)

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
        application.date_applied = data["date_applied"]

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
        "date_applied": application.date_applied,
        "job_url": application.job_url,
        "notes": application.notes,
        "salary": application.salary,
        "created_at": application.created_at
    })


if __name__ == "__main__":
    app.run(debug=True)