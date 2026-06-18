# Project Structure Overview

## Competitive Programming Contest Platform

This is a complete Flask + MySQL web application for managing competitive programming contests.

## Directory Tree

```
.
├── app/                          # Main Flask application package
│   ├── __init__.py              # Flask app initialization and setup
│   ├── routes/                  # Route blueprints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes (login, register, logout)
│   │   ├── contests.py          # Contest management routes
│   │   ├── problems.py          # Problem handling routes
│   │   ├── submissions.py       # Code submission routes
│   │   └── leaderboard.py       # Leaderboard display routes
│   ├── utils/                   # Utility modules
│   │   ├── db.py                # Database connection and initialization
│   │   └── auth.py              # Authentication utilities and decorators
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template with navbar and layout
│   │   ├── login.html           # Login page
│   │   ├── register.html        # User registration page
│   │   ├── contests/            # Contest-related templates
│   │   │   ├── list.html        # List all contests
│   │   │   ├── view.html        # View specific contest
│   │   │   └── create.html      # Create new contest form
│   │   ├── problems/            # Problem-related templates
│   │   │   ├── view.html        # View problem and submit solution
│   │   │   └── create.html      # Create problem form
│   │   ├── submissions/         # Submission-related templates
│   │   │   ├── view.html        # View single submission
│   │   │   └── my_submissions.html  # User's submission history
│   │   └── leaderboard/         # Leaderboard templates
│   │       ├── global.html      # Global leaderboard
│   │       └── contest.html     # Contest-specific leaderboard
│   └── static/                  # Static files
│       ├── css/                 # Stylesheets
│       │   └── style.css        # Main stylesheet with responsive design
│       └── js/                  # JavaScript files
│           └── main.js          # Client-side utilities and helpers
├── venv/                        # Python virtual environment (created during setup)
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── start.sh                     # Quick start script
├── README.md                    # Main documentation
├── SETUP.md                     # Setup and installation guide
└── PROJECT_STRUCTURE.md         # This file
```

## File Descriptions

### Core Application Files

#### `app/__init__.py`
- Initializes Flask application
- Registers all blueprints (routes)
- Sets up session secrets
- Calls database initialization

#### `run.py`
- Entry point for the Flask application
- Starts development server on `localhost:5000`
- Can be modified for production deployment

#### `requirements.txt`
- Lists all Python package dependencies
- Flask: Web framework
- mysql-connector-python: MySQL database driver
- Werkzeug: Password hashing utilities

### Routes (Blueprint Modules)

#### `app/routes/auth.py`
**Endpoints:**
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET /` - Index/redirect to login/contests

**Features:**
- User registration with validation
- Secure password hashing
- Session management
- Login required decorator

#### `app/routes/contests.py`
**Endpoints:**
- `GET /contests/` - List all contests
- `GET /contests/<id>` - View specific contest
- `GET/POST /contests/create` - Create new contest
- `POST /contests/<id>/register` - Register for contest

**Features:**
- Contest creation and management
- Contest registration
- Problem listing for contests
- User participation tracking

#### `app/routes/problems.py`
**Endpoints:**
- `GET /problems/<id>` - View problem details
- `GET/POST /problems/<id>/create` - Create problem

**Features:**
- Problem display with metadata
- Time and memory limits
- Difficulty levels
- Problem description rendering

#### `app/routes/submissions.py`
**Endpoints:**
- `POST /submissions/submit` - Submit code
- `GET /submissions/<id>` - View submission
- `GET /submissions/my` - View user submissions

**Features:**
- Code submission handling
- Simulated judging system
- Submission storage
- Mock results (Accept/WA/TLE/RE)

#### `app/routes/leaderboard.py`
**Endpoints:**
- `GET /leaderboard/` - Global leaderboard
- `GET /leaderboard/contest/<id>` - Contest leaderboard

**Features:**
- Global rankings
- Contest-specific rankings
- Score calculation
- Submission statistics

### Utility Modules

#### `app/utils/db.py`
**Functions:**
- `get_db_connection()` - Creates MySQL connection
- `init_database()` - Initializes all database tables

**Database Tables:**
- `users` - User accounts
- `contests` - Programming contests
- `problems` - Contest problems
- `submissions` - Code submissions
- `contest_registrations` - User registrations

#### `app/utils/auth.py`
**Functions:**
- `hash_password()` - Hashes passwords securely
- `verify_password()` - Verifies password against hash
- `register_user()` - Creates new user
- `authenticate_user()` - Validates login credentials
- `get_user_by_id()` - Retrieves user data
- `login_required` - Decorator for protected routes

### Templates

#### Base Template (`base.html`)
- Navigation bar with links
- User session display
- Flash message display
- Footer
- CSS and JS imports

#### Authentication Templates
- **login.html** - Login form with email/password
- **register.html** - Registration form with validation

#### Contest Templates
- **list.html** - Grid view of all contests with registration status
- **view.html** - Contest details with problem list
- **create.html** - Form to create new contest

#### Problem Templates
- **view.html** - Problem details and code submission form
- Shows problem description, constraints, and previous submissions

#### Submission Templates
- **view.html** - Displays code and judging result
- **my_submissions.html** - Table of user's all submissions

#### Leaderboard Templates
- **global.html** - Rankings across all contests
- **contest.html** - Rankings within specific contest

### Static Assets

#### CSS (`style.css`)
- Responsive design (mobile-first)
- Color scheme with CSS variables
- Component styling:
  - Buttons and forms
  - Cards and tables
  - Navigation
  - Alerts
  - Badges and status indicators
- Mobile breakpoints at 768px

#### JavaScript (`main.js`)
- Auto-dismiss alerts
- Form validation
- AJAX helpers
- Utility functions
- Date/time formatting

## Database Schema

### `users` Table
```sql
id (INT, PRIMARY KEY, AUTO_INCREMENT)
username (VARCHAR 50, UNIQUE)
email (VARCHAR 100, UNIQUE)
password_hash (VARCHAR 255)
full_name (VARCHAR 100)
created_at (TIMESTAMP)
```

### `contests` Table
```sql
id (INT, PRIMARY KEY, AUTO_INCREMENT)
creator_id (INT, FOREIGN KEY -> users.id)
title (VARCHAR 200)
description (TEXT)
start_time (DATETIME)
end_time (DATETIME)
created_at (TIMESTAMP)
```

### `problems` Table
```sql
id (INT, PRIMARY KEY, AUTO_INCREMENT)
contest_id (INT, FOREIGN KEY -> contests.id)
title (VARCHAR 200)
description (TEXT)
difficulty (VARCHAR 50)
time_limit (INT)
memory_limit (INT)
created_at (TIMESTAMP)
```

### `submissions` Table
```sql
id (INT, PRIMARY KEY, AUTO_INCREMENT)
user_id (INT, FOREIGN KEY -> users.id)
problem_id (INT, FOREIGN KEY -> problems.id)
code (LONGTEXT)
language (VARCHAR 50)
status (VARCHAR 50)
score (INT)
submitted_at (TIMESTAMP)
```

### `contest_registrations` Table
```sql
id (INT, PRIMARY KEY, AUTO_INCREMENT)
user_id (INT, FOREIGN KEY -> users.id)
contest_id (INT, FOREIGN KEY -> contests.id)
registered_at (TIMESTAMP)
UNIQUE(user_id, contest_id)
```

## Application Flow

```
1. User visits localhost:5000
   ├─ If logged in → Redirects to /contests/
   └─ If not logged in → Redirects to /login

2. Login/Registration
   ├─ POST to /register → Creates user account
   └─ POST to /login → Creates session

3. Contest Management
   ├─ GET /contests/ → Lists contests
   ├─ POST /contests/<id>/register → Registers user
   └─ GET /contests/<id> → Shows problems

4. Problem Solving
   ├─ GET /problems/<id> → Displays problem
   ├─ POST /submissions/submit → Submits code
   └─ Judging system → Simulates result

5. Leaderboard
   ├─ GET /leaderboard/ → Global rankings
   └─ GET /leaderboard/contest/<id> → Contest rankings

6. Logout
   └─ GET /logout → Clears session
```

## Key Features

### Security
- Password hashing with Werkzeug
- Session-based authentication
- Login required decorator for protected routes
- SQL parameter binding for SQL injection prevention

### Functionality
- User registration and authentication
- Contest creation and management
- Problem submission and storage
- Simulated code judging
- Leaderboard generation
- Submission history tracking

### User Experience
- Responsive design (mobile-friendly)
- Clean, modern interface
- Real-time form validation
- Helpful error messages
- Navigation between features

### Database
- Automatic table creation on startup
- Proper foreign key relationships
- Indexed unique constraints
- Transaction support

## Customization Points

### Add New Features
1. Create new route file in `app/routes/`
2. Create templates in `app/templates/`
3. Register blueprint in `app/__init__.py`

### Modify Styling
- Edit `app/static/css/style.css`
- CSS variables for theme colors
- Responsive breakpoints

### Change Database
- Modify connection in `app/utils/db.py`
- Update SQL schema in `init_database()`

### Enhance Judging
- Modify `simulate_judging()` in `app/routes/submissions.py`
- Add real code execution logic

## Running the Application

```bash
# Option 1: Using start script
./start.sh

# Option 2: Manual
source venv/bin/activate
python run.py
```

## Next Steps

1. Complete setup as per SETUP.md
2. Create user account
3. Create a contest
4. Add problems
5. Submit solutions
6. Check leaderboard

## Support

- See README.md for documentation
- See SETUP.md for installation help
- Review code comments for implementation details
