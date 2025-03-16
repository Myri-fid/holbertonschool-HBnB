#!/usr/bin/python3
"""
This file provides a User class
"""
import re
import uuid
from .base_class import Baseclass



class User(Baseclass):
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

    def display(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
    }

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or not value:
            raise TypeError("first name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("first name is too long")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value:
            raise TypeError("last name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("last name is too long")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not value:
            raise TypeError("email is required")
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        if not re.match(pattern, value):
            raise ValueError("email format is incorrect")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Admin must be True or False")
        self._is_admin = value

    @property
    def place(self):
        return self._place

    def add_place(self, value):
        self._place.append(value)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Hashes the password before storing it."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Password cannot be empty.")
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')


    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self._password:
            raise ValueError("Password has not been set.") 
        return bcrypt.check_password_hash(self._password, password)

    def display(self):
        """Returns user information without exposing the password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def to_dict(self):
        """Converts to dict while avoiding exposing the password"""
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
