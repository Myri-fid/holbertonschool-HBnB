#!/usr/bin/python3
"""
This file provides a User class mapped to the database.
"""
import re
from app import bcrypt
from .base_class import Baseclass
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, String, Boolean, Integer

class User(Baseclass):
    """
    This class represents a user in the system.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    places = relationship('Place', backref='owner', cascade="all, delete")
    # reviews = relationship('Review', backref='user', cascade="all, delete")

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        """ Ensures first and last names are valid before saving to DB """
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key.replace('_', ' ').title()} must be a non-empty string")
        if len(value) > 50:
            raise ValueError(f"{key.replace('_', ' ').title()} must be 50 characters or fewer")
        return value.capitalize()

    @validates('email')
    def validate_email(self, key, email):
        """ Ensures email format is valid before saving to DB """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not isinstance(email, str) or not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()

    def set_password(self, password):
        """Hashes and stores the password securely."""
        if not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

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
