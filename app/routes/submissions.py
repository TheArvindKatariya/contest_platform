from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.utils.auth import login_required
from app.utils.db import get_db_connection
import random

bp = Blueprint('submissions', __name__, url_prefix='/submissions')

def simulate_judging():
    """Simulate the judging process - returns random accept/reject with score"""
    statuses = ['Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Runtime Error']
    status = random.choice(statuses)
    score = 100 if status == 'Accepted' else random.randint(0, 50)
    return status, score

@bp.route('/submit', methods=['POST'])
@login_required
def submit_code():
    """Submit code for a problem"""
    data = request.get_json() if request.is_json else request.form
    problem_id = data.get('problem_id')
    code = data.get('code')
    language = data.get('language', 'Python')
    
    if not all([problem_id, code]):
        if request.is_json:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        return redirect(url_for('problems.view_problem', problem_id=problem_id))
    
    # Simulate judging
    status, score = simulate_judging()
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO submissions (user_id, problem_id, code, language, status, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session['user_id'], problem_id, code, language, status, score))
        connection.commit()
        
        submission_id = cursor.lastrowid
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Code submitted successfully',
                'submission_id': submission_id,
                'status': status,
                'score': score
            }), 200
        
        return redirect(url_for('problems.view_problem', problem_id=problem_id))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'message': str(e)}), 400
        return redirect(url_for('problems.view_problem', problem_id=problem_id))
    finally:
        cursor.close()
        connection.close()

@bp.route('/<int:submission_id>')
@login_required
def view_submission(submission_id):
    """View a specific submission"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT * FROM submissions WHERE id = ?
    """, (submission_id,))
    submission = cursor.fetchone()
    
    if not submission:
        cursor.close()
        connection.close()
        return "Submission not found", 404
    
    # Check if user owns this submission
    if submission['user_id'] != session['user_id']:
        cursor.close()
        connection.close()
        return "Unauthorized", 403
    
    cursor.close()
    connection.close()
    
    return render_template('submissions/view.html', submission=submission)

@bp.route('/my')
@login_required
def my_submissions():
    """View user's submissions"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT s.*, p.title as problem_title, c.title as contest_title
        FROM submissions s
        JOIN problems p ON s.problem_id = p.id
        JOIN contests c ON p.contest_id = c.id
        WHERE s.user_id = ?
        ORDER BY s.submitted_at DESC
    """, (session['user_id'],))
    
    submissions = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('submissions/my_submissions.html', submissions=submissions)
