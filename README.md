# Competitive Programming Contest Platform

A web-based platform for creating and participating in competitive programming contests built with Flask, MySQL, HTML, CSS, and JavaScript.

## Features

- **User Authentication**: Secure signup and login system
- **Contest Management**: Create and manage programming contests
- **Problem Submission**: Submit code solutions for problems
- **Code Judging**: Simulated judging system for submissions
- **Leaderboards**: Global and per-contest leaderboards
- **Submission History**: Track all your submissions

## Tech Stack

- **Backend**: Python + Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Password hashing with Werkzeug

## Project Structure

```
app/
├── __init__.py           # Flask app initialization
├── routes/               # Blueprint routes
│   ├── auth.py          # Authentication routes
│   ├── contests.py      # Contest management
│   ├── problems.py      # Problem handling
│   ├── submissions.py   # Code submissions
│   └── leaderboard.py   # Leaderboard views
├── utils/
│   ├── db.py            # Database utilities
│   └── auth.py          # Authentication utilities
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── contests/        # Contest templates
│   ├── problems/        # Problem templates
│   ├── submissions/     # Submission templates
│   └── leaderboard/     # Leaderboard templates
└── static/              # Static files
    ├── css/style.css    # Main stylesheet
    └── js/main.js       # Main JavaScript

run.py                   # Application entry point
requirements.txt         # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

Create a new MySQL database:

```bash
mysql -u root -p
CREATE DATABASE competitive_programming;
EXIT;
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update the database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your database details:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=competitive_programming
```

### 4. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### Creating an Account

1. Visit `http://localhost:5000`
2. Click "Sign Up"
3. Fill in your details and create an account
4. Login with your credentials

### Creating a Contest

1. Login to your account
2. Navigate to "Contests"
3. Click "Create Contest"
4. Fill in contest details (title, description, start/end times)
5. Click "Create"

### Participating in a Contest

1. Go to "Contests" page
2. Find a contest you want to join
3. Click "Register" to join the contest
4. View the contest to see available problems

### Submitting Solutions

1. Open a problem in a contest you're registered for
2. Select your programming language
3. Write or paste your code
4. Click "Submit"
5. View the judging result (simulated)

### Checking Leaderboard

- **Global Leaderboard**: See rankings of all users across all contests
- **Contest Leaderboard**: See rankings within a specific contest

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Contests
- `GET /contests/` - List all contests
- `GET /contests/<id>` - View specific contest
- `POST /contests/create` - Create new contest
- `POST /contests/<id>/register` - Register for contest

### Problems
- `GET /problems/<id>` - View problem details

### Submissions
- `POST /submissions/submit` - Submit code for a problem
- `GET /submissions/<id>` - View submission details
- `GET /submissions/my` - View user's submissions

### Leaderboard
- `GET /leaderboard/` - View global leaderboard
- `GET /leaderboard/contest/<id>` - View contest leaderboard

## Features Implemented (MVP)

- ✅ User Authentication (Signup/Login)
- ✅ Contest Creation & Management
- ✅ Problem Management
- ✅ Code Submission System
- ✅ Simulated Code Judging
- ✅ Global Leaderboard
- ✅ Contest-specific Leaderboard
- ✅ Submission History
- ✅ Responsive UI Design

## Future Enhancements

- Real code execution and judging
- Test case validation
- Code quality analysis
- Team contests
- Admin panel
- Email notifications
- Code formatting/beautification
- Plagiarism detection

## Security Notes

- Change the `SECRET_KEY` in `app/__init__.py` for production
- Use environment variables for sensitive data
- Implement rate limiting in production
- Add CSRF protection
- Use HTTPS in production

## Troubleshooting

### Database Connection Error

Ensure MySQL is running and your credentials in `.env` are correct:

```bash
mysql -u root -p -h localhost
```

### Port Already in Use

Change the port in `run.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Missing Dependencies

Reinstall requirements:

```bash
pip install -r requirements.txt --force-reinstall
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue or contact the development team.

## Contributors

Built with Python, Flask, and MySQL.
