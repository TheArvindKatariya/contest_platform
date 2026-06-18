# Competitive Programming Platform - Setup Guide

## Quick Start

### Option 1: Using start.sh (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This script will:
1. Create a Python virtual environment
2. Install all dependencies
3. Start the Flask server on `http://localhost:5000`

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Database

Edit `.env` file with your MySQL credentials:

```bash
cp .env.example .env
nano .env  # Edit with your database details
```

Configuration options:
```
DB_HOST=localhost          # MySQL server host
DB_USER=root               # MySQL username
DB_PASSWORD=               # MySQL password
DB_NAME=competitive_programming  # Database name
DB_PORT=3306               # MySQL port (default: 3306)
```

#### Step 4: Create MySQL Database

Open MySQL and create the database:

```bash
mysql -u root -p
CREATE DATABASE competitive_programming;
EXIT;
```

Or use this command:

```bash
mysql -u root -p -e "CREATE DATABASE competitive_programming;"
```

#### Step 5: Run the Application

```bash
python run.py
```

The app will be available at `http://localhost:5000`

## System Requirements

- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **pip**: Python package manager
- **RAM**: Minimum 512MB
- **Disk**: Minimum 100MB

## First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL server installed and running
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with MySQL credentials
- [ ] MySQL database created (`competitive_programming`)
- [ ] Flask server running on port 5000

## Troubleshooting

### 1. MySQL Connection Error

**Error**: `Can't connect to MySQL server`

**Solution**:
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Start MySQL if not running
sudo systemctl start mysql

# Verify credentials in .env file
cat .env
```

### 2. Port 5000 Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change the port in run.py:
# app.run(debug=True, host='0.0.0.0', port=5001)
```

### 3. Flask Module Not Found

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### 4. Permission Denied on start.sh

**Error**: `Permission denied`

**Solution**:
```bash
chmod +x start.sh
./start.sh
```

## Default Credentials

After setup, you can test with:

1. Create a new account at `http://localhost:5000/register`
2. Login with your credentials at `http://localhost:5000/login`

## Environment Variables

### Production Setup

For production deployment, set these environment variables:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-very-secure-random-key-here
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Development Setup (Default)

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Running on Different Port

Edit `run.py`:

```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change 8000 to your port
```

## Database Auto-Initialization

The database tables are automatically created when the Flask app starts. If you need to reset:

```python
from app.utils.db import init_database
init_database()
```

## Testing the Setup

1. **Check if server is running**:
   ```bash
   curl http://localhost:5000/
   ```

2. **Register a test account**:
   - Visit `http://localhost:5000/register`
   - Fill in details and submit

3. **Login**:
   - Visit `http://localhost:5000/login`
   - Use credentials you just created

4. **Create a contest**:
   - Click "Create Contest" button
   - Fill in details and submit

## Next Steps

1. **Add problems to contests**: Use the problem creation interface
2. **Customize the platform**: Edit CSS in `app/static/css/style.css`
3. **Add more features**: Check the `FUTURE_ENHANCEMENTS` section in README.md

## Support & Help

- Check README.md for API documentation
- Review code structure in the project directories
- Check Flask documentation: https://flask.palletsprojects.com/
- MySQL documentation: https://dev.mysql.com/doc/

## License

MIT License - Feel free to use and modify!
