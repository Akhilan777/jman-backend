from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return f"User id : {self.id}\nUser name : {self.name}\nUser username : {self.username}"
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Drivers(db.Model):
    __tablename__ = 'drivers'
    driver_id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(128), index=True, unique=True)
    driver_age = db.Column(db.Integer)
    driver_gender = db.Column(db.String(1))
    driver_address = db.Column(db.String(1024))
    driver_rating = db.Column(db.Float)
    bus_driving_experience = db.Column(db.Float)
    total_driving_experience = db.Column(db.Float)
    no_of_major_accidents = db.Column(db.Integer)
    no_of_minor_accidents = db.Column(db.Integer)
    average_driving_hours_in_day_time = db.Column(db.Float)
    average_driving_distance_in_day_time = db.Column(db.Float)
    average_driving_hours_in_night_time = db.Column(db.Float)
    average_driving_distance_in_night_time = db.Column(db.Float)
    safety_training_completed = db.Column(db.Boolean)
    prior_substance_use = db.Column(db.Boolean)
    vision_status = db.Column(db.String(64))
    health_status = db.Column(db.String(64))
    drivers = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Drivers {}>'.format(self.username)
    
class Routes(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.Integer, primary_key=True)
    route_name =db.Column(db.String(128), index=True)
    time =db.Column(db.String(64))
    date =db.Column(db.String(64))
    start =db.Column(db.String(64))
    destination =db.Column(db.String(64))
    driver_id = db.Column(db.Integer,db.ForeignKey('drivers.driver_id'))
    
    def __repr__(self):
        return '<Routes {}>'.format(self.body)
    
    
    
@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))