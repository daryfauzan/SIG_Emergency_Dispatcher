from datetime import datetime
from SIG_EmDis import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Dispatcher.query.get(int(id))

class Dispatcher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    isOnline = db.Column(db.Boolean, default=False, nullable=False)
    currCall = db.Column(db.Integer, default=0, nullable=False)
    pic = db.relationship('Call', backref='dispatcher', lazy=True)

    def __repr__(self):
        return str([self.id, self.name, self.isOnline, self.currCall])

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    destination = db.relationship('Call', backref='destination', lazy=True)

    def __repr__(self):
        return f"Hospital('{self.id}', '{self.name}', '{self.address}', '{self.phone_num}')"


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone_num = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, default='')
    status = db.Column(db.Integer, nullable=False, default=0)
    time_placed = db.Column(db.DateTime, nullable=False, default=datetime.now())
    time_response = db.Column(db.DateTime)
    time_completed = db.Column(db.DateTime)
    pic = db.Column(db.Integer, db.ForeignKey('dispatcher.id'), nullable=False)
    hospital = db.Column(db.Integer, db.ForeignKey('hospital.id'),nullable=False)

    def __repr__(self):
        return f"Call('{self.id}', '{self.phone_num}', '{self.message}')"



