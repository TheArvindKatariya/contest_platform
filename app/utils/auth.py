from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for
from app.utils.db import get_db_connection

def hash_password(password):
    """Hash a password using Werkzeug"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password_hash, password):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)

def register_user(username, email, password, full_name):
    """Register a new user"""
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed"
    
    cursor = connection.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, full_name))
        connection.commit()
        return True, "Registration successful"
    except Exception as e:
        if "Duplicate entry" in str(e) or "UNIQUE constraint failed" in str(e):
            return False, "Username or email already exists"
        return False, str(e)
    finally:
        cursor.close()
        connection.close()

def authenticate_user(username, password):
    """Authenticate user and return user data if successful"""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and verify_password(user['password_hash'], password):
            return user
        return None
    finally:
        cursor.close()
        connection.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, username, email, full_name FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
