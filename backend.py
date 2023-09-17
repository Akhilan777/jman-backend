from app import app, db
from app.models import Admin, Drivers, Routes


@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'Admin' : Admin, 'Drivers' : Drivers,'Routes':Routes}