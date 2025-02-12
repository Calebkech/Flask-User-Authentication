from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    expiry_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, username, password, is_admin=False, expiry_date=None):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.expiry_date = expiry_date

    def __repr__(self):
        return f"<email {self.username}>"
    