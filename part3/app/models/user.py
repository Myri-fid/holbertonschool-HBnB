#!/usr/bin/python3
"""
This file provides a User class
"""
import re
from app import db, bcrypt
from .base_class import Baseclass
from sqlalchemy.orm import relationship

class User(Baseclass, db.Model):
    """
    This class represents a user
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship('Place', backref='owner', cascade="all, delete")
    # reviews = relationship('Review', backref='user', cascade="all, delete")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """ Initializes a user with validation and transformation """
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.password = password
        self.is_admin = is_admin

    @staticmethod
    def validate_name(value, field_name):
        """ Checks that the first name/last name is not empty and is not too long """
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        if len(value) > 50:
            raise ValueError(f"{field_name} is too long")
        return value.capitalize()

    @staticmethod
    def validate_email(email):
        """ Checks the email format """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not isinstance(email, str) or not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """ Checks if the provided password matches the stored hash """
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """ Converts the object to a dictionary (excluding the password) """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
