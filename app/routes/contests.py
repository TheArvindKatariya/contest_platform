from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.utils.auth import login_required
from app.utils.db import get_db_connection
from datetime import datetime

bp = Blueprint('contests', __name__, url_prefix='/contests')

@bp.route('/')
@login_required
def list_contests():
    """List all contests"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get all contests with creator info
    cursor.execute("""
        SELECT c.*, u.username as creator_name
        FROM contests c
        JOIN users u ON c.creator_id = u.id
        ORDER BY c.start_time DESC
    """)
    contests = cursor.fetchall()
    
    # Get registered contests for current user
    cursor.execute("""
        SELECT contest_id FROM contest_registrations
        WHERE user_id = ?
    """, (session['user_id'],))
    registered = [row['contest_id'] for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    
    return render_template('contests/list.html', contests=contests, registered=registered)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_contest():
    """Create a new contest"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        title = data.get('title')
        description = data.get('description')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if not all([title, start_time, end_time]):
            message = "Missing required fields"
            if request.is_json:
                return jsonify({'success': False, 'message': message}), 400
            return render_template('contests/create.html', error=message)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO contests (creator_id, title, description, start_time, end_time)
                VALUES (?, ?, ?, ?, ?)
            """, (session['user_id'], title, description, start_time, end_time))
            connection.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Contest created successfully'}), 200
            return redirect(url_for('contests.list_contests'))
        except Exception as e:
            message = str(e)
            if request.is_json:
                return jsonify({'success': False, 'message': message}), 400
            return render_template('contests/create.html', error=message)
        finally:
            cursor.close()
            connection.close()
    
    return render_template('contests/create.html')

@bp.route('/<int:contest_id>')
@login_required
def view_contest(contest_id):
    """View a specific contest"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Get contest details
    cursor.execute("""
        SELECT c.*, u.username as creator_name
        FROM contests c
        JOIN users u ON c.creator_id = u.id
        WHERE c.id = ?
    """, (contest_id,))
    contest = cursor.fetchone()
    
    if not contest:
        cursor.close()
        connection.close()
        return "Contest not found", 404
    
    # Get problems in this contest
    cursor.execute("""
        SELECT * FROM problems WHERE contest_id = ?
        ORDER BY id
    """, (contest_id,))
    problems = cursor.fetchall()
    
    # Check if user is registered
    cursor.execute("""
        SELECT * FROM contest_registrations
        WHERE user_id = ? AND contest_id = ?
    """, (session['user_id'], contest_id))
    is_registered = cursor.fetchone() is not None
    
    cursor.close()
    connection.close()
    
    return render_template('contests/view.html', contest=contest, problems=problems, is_registered=is_registered)

@bp.route('/<int:contest_id>/register', methods=['POST'])
@login_required
def register_contest(contest_id):
    """Register for a contest"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO contest_registrations (user_id, contest_id)
            VALUES (?, ?)
        """, (session['user_id'], contest_id))
        connection.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Registered successfully'}), 200
        return redirect(url_for('contests.view_contest', contest_id=contest_id))
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'message': str(e)}), 400
        return redirect(url_for('contests.view_contest', contest_id=contest_id))
    finally:
        cursor.close()
        connection.close()
