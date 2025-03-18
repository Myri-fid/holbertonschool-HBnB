#!/usr/bin/python3
"""This module defines the Amenity class."""

import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import validates, relationship
from app.models.base_class import Baseclass
from app import db


class Amenity(Baseclass):
    """Defines attributes and methods for the Amenity class."""

    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)

    @validates('name')
    def validate_name(self, key, value):
        """Ensures the name is valid before saving to the database."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "Amenity name is required and must be a non-empty string"
                )
        if len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        return value.capitalize()

    def update_timestamp(self):
        """Updates the `updated_at` timestamp before committing changes."""
        self.updated_at = db.func.current_timestamp()
        db.session.commit()

    def to_dict(self):
        """Returns a dictionary representation of the Amenity object."""
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return f"Amenity: {self.name} (ID: {self.id})"
