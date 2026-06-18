# Installation & Running the App

## System Information
- **Database**: SQLite (no setup needed, built-in to Python)
- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript
- **Port**: 5000

---

## Quick Start (3 Steps)

### 1. Navigate to Project
```bash
cd /vercel/share/v0-project
```

### 2. Create Virtual Environment (First Time Only)
```bash
python3 -m venv venv
```

### 3. Run the App
```bash
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## Next: Open in Browser

Visit: **http://localhost:5000**

You should see the login page.

---

## First Time Using the App

### Create Account
1. Click **"Sign Up"** link
2. Fill in:
   - Username
   - Email
   - Password
3. Click **"Register"**

### Create a Contest
1. Go to **"Contests"** menu
2. Click **"Create Contest"**
3. Fill in contest details:
   - Title
   - Description
   - Start date/time
   - End date/time
4. Click **"Create"**

### Add Problems to Contest
1. View your contest
2. Click **"Add Problem"**
3. Enter problem details and save

### Submit Solutions
1. Register for a contest
2. View problems
3. Submit code
4. Check leaderboard

---

## Complete Setup Instructions (First Time)

### Step 1: Install Dependencies
```bash
cd /vercel/share/v0-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Werkzeug (security)
- python-dotenv (environment config)

### Step 2: Create Environment File
```bash
# Already created at .env
# Edit if needed:
nano .env
```

Current settings:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-me-in-production
PORT=5000
```

### Step 3: Start Server
```bash
source venv/bin/activate
python run.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

---

## Stopping the Server

Press **CTRL+C** in the terminal.

---

## Subsequent Runs

After the first setup, just do:

```bash
cd /vercel/share/v0-project
source venv/bin/activate
python run.py
```

The database persists, so your data is saved between runs.

---

## Troubleshooting

### Port 5000 Already in Use

**On macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

**On Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Or use a different port:**

Edit `run.py`:
```python
port = int(os.getenv('PORT', 8080))  # Change 5000 to 8080
```

### Virtual Environment Issues

**Venv not working:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Python not found:**
```bash
# Make sure Python 3 is installed
python3 --version

# Use python3 explicitly
python3 run.py
```

### Permission Denied on start.sh

```bash
chmod +x start.sh
./start.sh
```

---

## What Gets Created

When you run the app for the first time:

1. **contest_platform.db** - SQLite database file (data persists)
2. Database tables for users, contests, problems, submissions
3. Any uploaded/generated files

---

## Database

- **Type**: SQLite
- **Location**: `contest_platform.db` in project root
- **No setup needed**: Automatically created on first run
- **Data persists**: Between app restarts

To reset database:
```bash
rm contest_platform.db
python run.py
```

---

## Environment Variables

Edit `.env` file to change:

```
FLASK_ENV=development      # Change to 'production' for deployment
FLASK_DEBUG=True           # Change to 'False' for production
SECRET_KEY=your-key        # Change this for production
PORT=5000                  # Change port number
```

---

## File Locations

```
.env                    # Configuration
run.py                  # Main entry point
requirements.txt        # Dependencies
contest_platform.db     # Database (created on first run)
app/
├── routes/             # API endpoints
├── templates/          # HTML pages
├── static/             # CSS/JavaScript
└── utils/              # Database utilities
```

---

## Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# See installed packages
pip list

# Freeze dependencies
pip freeze > requirements.txt
```

---

## Performance Notes

- SQLite works great for development and small deployments
- For large production deployments, consider MySQL/PostgreSQL
- Database file grows with usage (currently should be small)

---

## Features Available

✓ User authentication (signup/login)
✓ Create/manage contests
✓ Add problems with descriptions
✓ Submit code in 5 languages
✓ Simulated code judging
✓ Global leaderboard
✓ Contest-specific leaderboards
✓ Responsive mobile design
✓ User submissions history

---

## Next Steps

1. Create an account at http://localhost:5000/register
2. Create a test contest
3. Add problems
4. Submit solutions
5. Check leaderboard

Enjoy! 🎉

---

For full documentation, see:
- **README.md** - Complete documentation
- **PROJECT_STRUCTURE.md** - Code organization
- **DOCS_INDEX.md** - All documentation files
