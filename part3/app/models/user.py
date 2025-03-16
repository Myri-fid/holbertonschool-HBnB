#!/usr/bin/python3
"""
This file provides a User class
"""

import re
from .base_class import Baseclass
from app import db, bcrypt

class User(Baseclass, db.Model):
    """
    This class represents a user
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Password cannot be empty.")
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    def verify_password(self, password):
        if not self._password:
            raise ValueError("Password has not been set.") 
        return bcrypt.check_password_hash(self._password, password)

    def display(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def to_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
