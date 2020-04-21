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

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}', 'Online Status:{self.isOnline}')"