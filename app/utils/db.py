import sqlite3
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Try to import mysql.connector
try:
    import mysql.connector
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'contest_platform.db')

class UnifiedConnection:
    def __init__(self, conn, is_mysql=False):
        self.conn = conn
        self.is_mysql = is_mysql

    def cursor(self):
        if self.is_mysql:
            return UnifiedCursor(self.conn.cursor(dictionary=True), is_mysql=True)
        else:
            return UnifiedCursor(self.conn.cursor(), is_mysql=False)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class UnifiedCursor:
    def __init__(self, cursor, is_mysql=False):
        self.cursor = cursor
        self.is_mysql = is_mysql

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    def execute(self, query, params=None):
        if self.is_mysql:
            # Translate SQLite placeholders to MySQL
            if '?' in query:
                query = query.replace('?', '%s')
            if 'AUTOINCREMENT' in query:
                query = query.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
        else:
            # SQLite does not support AUTO_INCREMENT, only AUTOINCREMENT
            if 'AUTO_INCREMENT' in query:
                query = query.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
                
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

def get_db_connection():
    """Create and return a Unified database connection (MySQL or SQLite)"""
    # Check if MySQL credentials are provided in env and mysql.connector is available
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_db = os.getenv('MYSQL_DB')

    if HAS_MYSQL and all([mysql_host, mysql_user, mysql_db]):
        try:
            # Try connecting to MySQL
            conn = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database=mysql_db
            )
            return UnifiedConnection(conn, is_mysql=True)
        except Exception as e:
            print(f"Failed to connect to MySQL: {e}. Falling back to SQLite...")
    
    # Fallback to SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return UnifiedConnection(conn, is_mysql=False)
    except Exception as e:
        print(f"Error connecting to SQLite database: {e}")
        return None

def init_database():
    """Initialize database schema"""
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database for initialization")
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create contests table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            start_time DATETIME,
            end_time DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id)
        )
        """)
        
        # Create problems table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            difficulty VARCHAR(50),
            time_limit INTEGER DEFAULT 1,
            memory_limit INTEGER DEFAULT 256,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contest_id) REFERENCES contests(id) ON DELETE CASCADE
        )
        """)
        
        # Create submissions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            code TEXT,
            language VARCHAR(50),
            status VARCHAR(50) DEFAULT 'Pending',
            score INTEGER DEFAULT 0,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (problem_id) REFERENCES problems(id)
        )
        """)
        
        # Create contest_registrations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contest_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            contest_id INTEGER NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (user_id, contest_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (contest_id) REFERENCES contests(id) ON DELETE CASCADE
        )
        """)
        
        connection.commit()
        print("Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
