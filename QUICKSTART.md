# Quick Start Guide - Competitive Programming Platform

## What You Have

A complete, production-ready Competitive Programming Contest Platform built with:
- **Backend**: Python + Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Auth**: Secure password hashing with Werkzeug

## Get Started in 5 Minutes

### 1. Start the Server (First Time)

```bash
# Make the start script executable
chmod +x start.sh

# Run it
./start.sh
```

This script will:
- Create a Python virtual environment
- Install all dependencies
- Start the Flask server

Visit: **http://localhost:5000**

### 2. Quick Setup Checklist

Before running the server, make sure:
- [ ] Python 3.8+ is installed: `python3 --version`
- [ ] MySQL is running: `mysql -u root -p` (can connect)
- [ ] You have at least 100MB free disk space

### 3. Create an Account

1. Go to http://localhost:5000
2. Click **"Sign Up"**
3. Fill in your details:
   - Full Name: Your name
   - Username: Your username
   - Email: Your email
   - Password: Your password
4. Click **"Register"**
5. Login with your credentials

### 4. Create Your First Contest

1. After login, click **"Contests"**
2. Click **"Create Contest"** button
3. Fill in:
   - **Title**: My First Contest
   - **Description**: A test contest
   - **Start Time**: Pick any future date/time
   - **End Time**: Pick a later date/time
4. Click **"Create"**

### 5. Add Problems

1. Go to your contest
2. You can now add problems to it
3. Each problem should have:
   - Title (e.g., "Hello World")
   - Description
   - Difficulty (Easy/Medium/Hard)
   - Time Limit (seconds)
   - Memory Limit (MB)

### 6. Solve Problems

1. Register for a contest you created
2. Click on a problem
3. Select language (Python, C++, Java, etc.)
4. Write your code
5. Click **"Submit"**
6. Check the result (simulated judging)

### 7. Check Leaderboards

- **Global**: See top performers across all contests
- **Per-Contest**: See rankings within specific contests
- Sorted by total score and number of accepted problems

## Features Available Now

✅ User Accounts (signup/login)
✅ Create/Manage Contests
✅ Add Problems
✅ Submit Solutions
✅ Code Judging (simulated with Accept/WA/TLE/RTE)
✅ Global Leaderboard
✅ Contest Leaderboards
✅ Submission History
✅ Responsive Mobile Design

## File Structure

```
app/
├── routes/         # All the endpoints (login, contests, problems, etc.)
├── templates/      # HTML pages
├── static/         # CSS and JavaScript
└── utils/          # Database and auth helpers

run.py             # Start the app
start.sh           # Quick start script
requirements.txt   # Python packages needed
.env.example       # Database config template
```

## Common Tasks

### Task: Run Server Again

```bash
./start.sh
```

Or manually:
```bash
source venv/bin/activate
python run.py
```

### Task: Change Server Port

Edit `run.py`, change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to your port
```

### Task: Stop the Server

Press `Ctrl+C` in the terminal where Flask is running.

### Task: Add More Users

Send them to: `http://localhost:5000/register`
They can create their own accounts.

### Task: Add Real Code Judging

Edit `app/routes/submissions.py`, replace `simulate_judging()` function with real execution logic.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to MySQL | Start MySQL: `sudo systemctl start mysql` |
| Port 5000 in use | Kill process: `lsof -ti:5000 \| xargs kill -9` |
| "Flask not found" | Run: `pip install -r requirements.txt` |
| Database error | Ensure MySQL is running and `.env` has correct credentials |
| Page shows 404 | Make sure you're logged in before accessing /contests |

## URL Cheat Sheet

| URL | Purpose |
|-----|---------|
| http://localhost:5000/ | Home (redirects to login or contests) |
| http://localhost:5000/register | Create account |
| http://localhost:5000/login | Login |
| http://localhost:5000/logout | Logout |
| http://localhost:5000/contests/ | View all contests |
| http://localhost:5000/contests/create | Create new contest |
| http://localhost:5000/leaderboard/ | Global rankings |
| http://localhost:5000/submissions/my | Your submissions |

## Customization

### Change Theme Colors

Edit `app/static/css/style.css`, modify CSS variables:
```css
:root {
    --primary-color: #2563eb;      /* Blue - change to any color */
    --secondary-color: #64748b;    /* Gray */
    --success-color: #10b981;      /* Green */
    --error-color: #ef4444;        /* Red */
}
```

### Change Platform Name

Edit `app/templates/base.html`:
```html
<a href="/">CP Platform</a>  <!-- Change "CP Platform" to your name -->
```

### Modify Database

Edit `app/utils/db.py`:
```python
def init_database():
    # Add your custom SQL tables here
```

## For Production

1. Change `SECRET_KEY` in `app/__init__.py`
2. Set `FLASK_ENV=production`
3. Set `FLASK_DEBUG=0`
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Set up a reverse proxy (Nginx)
6. Use HTTPS/SSL certificates

## Need Help?

- **Setup Issues**: See `SETUP.md`
- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **API Documentation**: See `README.md`
- **Code Comments**: Review code in `app/routes/` and `app/utils/`

## What's Next?

1. **Test the platform** - Create contests, submit code
2. **Customize the UI** - Edit templates and CSS
3. **Add real judging** - Replace simulated judging with real code execution
4. **Deploy online** - Use services like Heroku, AWS, or DigitalOcean
5. **Add features** - Check `README.md` for ideas

## Features to Add Later

- Real code execution and testing
- Team contests
- Problem difficulty statistics
- User profiles
- Email notifications
- Admin dashboard
- Code plagiarism detection
- Discussion forums

## One-Command Start (Next Time)

```bash
./start.sh && echo "App running at http://localhost:5000"
```

---

**Enjoy building!** 🚀

Have questions? Check the documentation files:
- `SETUP.md` - Installation help
- `README.md` - Full documentation
- `PROJECT_STRUCTURE.md` - Code organization
