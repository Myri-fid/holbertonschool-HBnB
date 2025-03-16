#!/usr/bin/python3
"""This module defines the Amenity class."""

import uuid
from datetime import datetime
from app.models.base_class import Baseclass
from app import db

class Amenity(Baseclass, db.Model):
    """Defines attributes and methods for the Amenity class."""
    
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The name of the amenity is required and must be a string")
        if len(name) > 50:
            raise ValueError("The name of the amenity cannot exceed 50 characters")

        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()
