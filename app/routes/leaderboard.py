from flask import Blueprint, render_template, session
from app.utils.auth import login_required
from app.utils.db import get_db_connection

bp = Blueprint('leaderboard', __name__, url_prefix='/leaderboard')

@bp.route('/')
@login_required
def global_leaderboard():
    """View global leaderboard"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get top users by total score
    cursor.execute("""
        SELECT u.id, u.username, COUNT(DISTINCT s.id) as submissions,
               SUM(CASE WHEN s.status = 'Accepted' THEN 1 ELSE 0 END) as accepted,
               SUM(s.score) as total_score
        FROM users u
        LEFT JOIN submissions s ON u.id = s.user_id
        GROUP BY u.id, u.username
        ORDER BY total_score DESC, accepted DESC
        LIMIT 100
    """)
    
    leaderboard = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('leaderboard/global.html', leaderboard=leaderboard)

@bp.route('/contest/<int:contest_id>')
@login_required
def contest_leaderboard(contest_id):
    """View leaderboard for a specific contest"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get contest details
    cursor.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
    contest = cursor.fetchone()
    
    if not contest:
        cursor.close()
        connection.close()
        return "Contest not found", 404
    
    # Get leaderboard for this contest
    cursor.execute("""
        SELECT u.id, u.username,
               COUNT(DISTINCT s.id) as submissions,
               SUM(CASE WHEN s.status = 'Accepted' THEN 1 ELSE 0 END) as accepted,
               SUM(s.score) as total_score
        FROM contest_registrations cr
        JOIN users u ON cr.user_id = u.id
        LEFT JOIN submissions s ON u.id = s.user_id
        LEFT JOIN problems p ON s.problem_id = p.id
        WHERE cr.contest_id = ? AND p.contest_id = ?
        GROUP BY u.id, u.username
        ORDER BY total_score DESC, accepted DESC
    """, (contest_id, contest_id))
    
    leaderboard = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('leaderboard/contest.html', contest=contest, leaderboard=leaderboard)
