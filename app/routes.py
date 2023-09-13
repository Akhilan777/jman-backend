from app import app, db
from flask import jsonify
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
