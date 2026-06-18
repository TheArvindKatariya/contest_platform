from flask import Flask
from app.utils.db import init_database

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = 'your-secret-key-change-in-production'
    
    # Initialize database
    init_database()
    
    # Register blueprints
    from app.routes import auth, contests, problems, submissions, leaderboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(contests.bp)
    app.register_blueprint(problems.bp)
    app.register_blueprint(submissions.bp)
    app.register_blueprint(leaderboard.bp)
    
    return app
