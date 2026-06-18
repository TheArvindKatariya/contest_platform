from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.utils.auth import login_required
from app.utils.db import get_db_connection

bp = Blueprint('problems', __name__, url_prefix='/problems')

@bp.route('/<int:problem_id>')
@login_required
def view_problem(problem_id):
    """View a specific problem"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get problem details
    cursor.execute("""
        SELECT p.*, c.id as contest_id
        FROM problems p
        JOIN contests c ON p.contest_id = c.id
        WHERE p.id = ?
    """, (problem_id,))
    problem = cursor.fetchone()
    
    if not problem:
        cursor.close()
        connection.close()
        return "Problem not found", 404
    
    # Check if user is registered for the contest
    cursor.execute("""
        SELECT * FROM contest_registrations
        WHERE user_id = ? AND contest_id = ?
    """, (session['user_id'], problem['contest_id']))
    is_registered = cursor.fetchone() is not None
    
    # Check if user is the contest creator (organiser)
    cursor.execute("SELECT creator_id FROM contests WHERE id = ?", (problem['contest_id'],))
    contest = cursor.fetchone()
    is_creator = contest and contest['creator_id'] == session['user_id']
    
    # Get user's previous submissions for this problem
    cursor.execute("""
        SELECT * FROM submissions
        WHERE user_id = ? AND problem_id = ?
        ORDER BY submitted_at DESC
        LIMIT 5
    """, (session['user_id'], problem_id))
    submissions = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    if not is_registered and not is_creator:
        return "You are not registered for this contest", 403
    
    return render_template('problems/view.html', problem=problem, submissions=submissions)

@bp.route('/create/<int:contest_id>', methods=['GET', 'POST'])
@login_required
def create_problem(contest_id):
    """Create a problem (for contest creator/organiser)"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get contest details to verify ownership
    cursor.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
    contest = cursor.fetchone()
    
    if not contest:
        cursor.close()
        connection.close()
        return "Contest not found", 404
        
    if contest['creator_id'] != session['user_id']:
        cursor.close()
        connection.close()
        return "Unauthorized: Only the contest creator can add problems", 403
        
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        title = data.get('title')
        description = data.get('description')
        difficulty = data.get('difficulty', 'Medium')
        time_limit = data.get('time_limit', 1)
        memory_limit = data.get('memory_limit', 256)
        
        if not title:
            error = "Title is required"
            if request.is_json:
                return jsonify({'success': False, 'message': error}), 400
            return render_template('problems/create.html', contest=contest, error=error)
            
        try:
            cursor.execute("""
                INSERT INTO problems (contest_id, title, description, difficulty, time_limit, memory_limit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contest_id, title, description, difficulty, time_limit, memory_limit))
            connection.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Problem created successfully'}), 200
            return redirect(url_for('contests.view_contest', contest_id=contest_id))
        except Exception as e:
            if request.is_json:
                return jsonify({'success': False, 'message': str(e)}), 400
            return render_template('problems/create.html', contest=contest, error=str(e))
        finally:
            cursor.close()
            connection.close()
            
    cursor.close()
    connection.close()
    return render_template('problems/create.html', contest=contest)
