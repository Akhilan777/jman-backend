from app import app, db
from app.models import Admin, Drivers,Routes
from flask import request, jsonify,render_template
from flask_login import current_user, login_user, logout_user
from sqlalchemy import text

@app.route('/')
def test():
    return {'message' : "hello, world"}

@app.route('/test_database_connection')
def test_database_connection():
    try:
        result = db.session.execute(text('SELECT version()'))
        version = result.scalar()
        return jsonify({'message' : 'Database connection successful', 'version' : version}), 200
    except Exception as e:
        return jsonify({'message' : 'Database connection failed', 'error' : str(e)}), 500
    

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'loggedIn' : True, 'username' : current_user.username}), 200
    
    username = request.json.get('username')
    password = request.json.get('password')
    remember_me = request.json.get('remember_me')
    user = Admin.query.filter_by(username=username).first()

    if user is None or not user.check_password(password=password):
        return jsonify({'message' : 'Login failed', 'reason' : 'Invalid username or password'}), 401
    
    login_user(user, remember=remember_me)
    return jsonify({'message' : 'Login successful'}), 200

@app.route('/driver/<int:driver_id>/')
def driver(driver_id):
    d = Drivers.query.get_or_404(driver_id)
    return jsonify(d.serialize())

@app.route('/route/<int:route_id>/')
def route(route_id):
    r=Routes.query.get_or_404(route_id)
    return jsonify(r.serialize())

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'message' : 'Logout Successful'}), 200