import uuid
from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID stored as string
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    amount = db.Column(db.Float, nullable=False, default=0)
    created_by = db.Column(db.String(50), nullable=False, default='admin')
    expiry_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, username, password, is_admin=False, expiry_date=None, amount=0, created_by='admin'):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.expiry_date = expiry_date
        self.amount = amount
        self.created_by = created_by

    def __repr__(self):
        return f"<email {self.username}>"
