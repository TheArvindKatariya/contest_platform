from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.utils.auth import register_user, authenticate_user, login_required

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        success, message = register_user(username, email, password, full_name)
        
        if request.is_json:
            return jsonify({'success': success, 'message': message}), 200 if success else 400
        
        if success:
            return redirect(url_for('auth.login'))
        return render_template('register.html', error=message)
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Login successful'}), 200
            return redirect(url_for('contests.list_contests'))
        
        message = "Invalid username or password"
        if request.is_json:
            return jsonify({'success': False, 'message': message}), 401
        return render_template('login.html', error=message)
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('contests.list_contests'))
    return redirect(url_for('auth.login'))
