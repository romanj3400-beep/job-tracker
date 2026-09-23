from app import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)

    position = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100))

    status = db.Column(db.String(50), nullable=False, default="Applied")

    date_applied = db.Column(db.Date)

    follow_up_date = db.Cloumn(db.Date)

    salary = db.Column(db.Integer)

    job_url = db.Column(db.String(500))

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

   
