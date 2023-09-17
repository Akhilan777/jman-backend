from app import db, login
from datetime import datetime, date, time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect


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
    drivers = db.relationship('Routes', backref='author', lazy='dynamic')
    
    def serialize(self):
        return {"driver_id": self.driver_id,
                "driver_name": self.driver_name,
                "driver_age":self.driver_age,
                "driver_gender":self.driver_gender,
                "driver_address":self.driver_address,
                "driver_rating":self.driver_rating,
                "bus_driving_experience":self.bus_driving_experience,
                "total_driving_experience":self. total_driving_experience,
                "no_of_major_accidents":self.no_of_major_accidents,
                "no_of_minor_accidents":self.no_of_minor_accidents,
                "average_driving_hours_in_day_time":self.average_driving_hours_in_day_time,
                "average_driving_distance_in_day_time":self.average_driving_distance_in_day_time,
                "average_driving_hours_in_night_time":self.average_driving_hours_in_night_time,
                "average_driving_distance_in_night_time":self.average_driving_distance_in_night_time,
                "safety_training_completed":self.safety_training_completed,
                "prior_substance_use":self.prior_substance_use,
                "vision_status":self.vision_status,
                "health_status":self.health_status}

    def __repr__(self):
        return '<Drivers {}>'.format(self.driver_id)

    def get_input(self, id):
        driver = Drivers.query.get(id)

        string_cols = ["driver_name", "driver_gender", "driver_address", "vision_status",
    "health_status"]

        int_cols = ["driver_age", "no_of_major_accidents", "no_of_minor_accidents"]

        boolean_cols = ["safety_training_completed" ,
    "prior_substance_use"]
        
        float_cols = ["driver_rating", 
                "bus_driving_experience", "total_driving_experience",
    "average_driving_hours_in_day_time" ,
    "average_driving_distance_in_day_time", 
    "average_driving_hours_in_night_time"  ,
    "average_driving_distance_in_night_time"
    ]
        
        for col in string_cols:
            val = input(f"Enter {col}: ").strip()
            setattr(self, col, val)

        
        for col in int_cols:
            print("ONLY INTEGER VALUES PLEASE")
            val = int( input(f"Enter {col}: ").strip())
            setattr(self, col, val)

        for col in boolean_cols:
            print("Enter 0 for False. 1 for True")
            val = int(input(f"Enter {col}: "))
            if(val == 0):
                setattr(self, col, False)
            else:
                setattr(self, col, True)

        for col in float_cols:
            print("ONLY NUMBERS PLEASE")
            val = float( input(f"Enter {col}: ").strip())
            setattr(self, col, val)
        

    
class Routes(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.Integer, primary_key=True)
    route_name =db.Column(db.String(128), index=True)
    date =db.Column(db.Date())
    time =db.Column(db.Time())
    start =db.Column(db.String(64))
    destination =db.Column(db.String(64))
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.driver_id'))
    
    def __repr__(self):
        return '<Routes {}>'.format(self.route_id)
    
    def serialize(self):
        return {"route_id": self.route_id,
                "route_name": self.route_name,
                "date":self.date,
                "time":self.time,
                "start":self.start,
                "destination":self.destination,
                "driver_id":self.driver_id}
    
    
    def get_input(self, id):
        route = Routes.query.get(id)

        string_cols = ["route_name", "start", "destination"]
        for col in string_cols:
            val = input(f"Enter {col}: ").strip()
            setattr(self, col, val)

        print("Date")
        date_input = input("Enter date in (dd-mm-yyyy): ")
        date_obj = datetime.strptime(date_input, "%d-%m-%Y").date()
        setattr(self, 'date', date_obj)

        print("Time")
        time_input = input("Enter time in (HH:MM:SS): ")
        time_obj = datetime.strptime(time_input, "%H:%M:%S").time()
        setattr(self, 'time', time_obj)

        driver_id_input = int(input("Enter driver id: "))
        setattr(self, 'driver_id', driver_id_input)

        
    
@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))