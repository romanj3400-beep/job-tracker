# Job Tracker

A full-stack web application for organizing and managing job applications in one place. Job Tracker allows users to track their applications, monitor their progress, record important details, and manage follow-up dates throughout their job search.

This project was built to strengthen my skills in Python, backend development, relational databases, REST APIs, and frontend development.

## Features

- **User Authentication:** Register an account and log in to access the application.
- **Application Management:** Record and manage job applications in one place.
- **Application Details:** Store company names, job titles, locations, application dates, salaries, job posting URLs, and notes.
- **Status Tracking:** Keep track of application progress, including statuses such as applied, interviewing, and offers.
- **Follow-Up Dates:** Record follow-up dates to help stay organized during the hiring process.
- **Database Integration:** Store application data in a MySQL database using SQLAlchemy.
- **Interactive Dashboard:** View and manage job application information through a web-based interface.

## Tech Stack

**Frontend**
- HTML5
- CSS3
- JavaScript

**Backend**
- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS

**Database**
- MySQL
- SQLAlchemy ORM

**Tools & Environment**
- Git and GitHub
- Ubuntu / WSL
- Python virtual environments
- Visual Studio Code

## Project Structure

```text
job-tracker/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── login.js
│   ├── script.js
│   └── style.css
└── README.md
```
The `.env` file contains local configuration and database credentials and should not be committed to GitHub. The virtual environment is also local to the development machine.

## Getting Started

Follow these instructions to run Job Tracker locally.

### Prerequisites

Make sure you have the following installed:

- Python 3
- MySQL Server
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd job-tracker
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the HTTPS or SSH URL of your GitHub repository.

### 2. Configure the MySQL Database

Open MySQL using an account with permission to create databases and users.

Create the database and, if needed, a dedicated database user:

```sql
CREATE DATABASE jobtrack;

CREATE USER 'jobtrack_user'@'localhost'
IDENTIFIED BY 'YOUR_DATABASE_PASSWORD';

GRANT ALL PRIVILEGES ON jobtrack.*
TO 'jobtrack_user'@'localhost';

FLUSH PRIVILEGES;
```

If the database or user already exists, you do not need to create it again. Use the existing account and credentials instead.

### 3. Set Up the Backend

Open a terminal in the project directory and run:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure the backend environment variables in `backend/.env`:

```env
SECRET_KEY=replace_with_a_long_random_secret
DATABASE_URL=your_mysql_connection_string
```

Replace the placeholders with your own values. The database connection string must match the MySQL driver and connection format configured for the project.

**Security note:** Never commit your `.env` file, database passwords, or production secret keys to GitHub.

### 4. Start the Flask Backend

From the `backend` directory, with the virtual environment activated, run:

```bash
python3 app.py
```

The backend should be available at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while using the application.

### 5. Start the Frontend

Open a second terminal and run:

```bash
cd ~/GitHub/job-tracker/frontend
python3 -m http.server 5500
```

Keep this terminal running as well.

### 6. Open Job Tracker

Open your browser and navigate to:

```text
http://127.0.0.1:5500/login.html
```

Register or log in to access the application.

**Important:** Serve the frontend through the local HTTP server instead of opening the HTML files directly using a `file://` address. The frontend communicates with the Flask backend, and the backend must be running for API requests to work.

## How It Works

Job Tracker uses a frontend-backend architecture:

1. The user interacts with the HTML, CSS, and JavaScript interface.
2. JavaScript sends HTTP requests to the Flask API.
3. Flask processes requests and interacts with the MySQL database through SQLAlchemy.
4. The backend returns responses that the frontend uses to update the interface.

The application also uses session-based authentication and credentialed requests to support authenticated interactions between the frontend and backend.

## What I Learned

Building this project has given me hands-on experience with:

- Developing a backend using Python and Flask.
- Designing and interacting with a relational MySQL database.
- Using SQLAlchemy to work with database models and records.
- Connecting frontend JavaScript to backend API endpoints.
- Implementing user registration and login functionality.
- Managing environment variables and database credentials.
- Debugging HTTP requests, CORS configuration, and frontend-backend communication.
- Using Git and GitHub to manage a software project.

## Future Improvements

Potential improvements include:

- Adding search, filtering, and sorting options for job applications.
- Improving dashboard statistics and application insights.
- Adding reminders for upcoming follow-up dates.
- Improving form validation and error handling.
- Adding automated backend and frontend tests.
- Deploying the application so it can be accessed outside the local development environment.

## Author

Developed as a personal full-stack software development project.


