import uuid
from datetime import datetime
from app.models.base_class import Baseclass
from app import db
from sqlalchemy.orm import relationship

class Place(Baseclass, db.Model):
    """
    Place class representing a location available for rent.
    """
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, default=0)

    owner = relationship('User', back_populates='places')
    reviews = relationship('Review', back_populates='place', cascade="all, delete-orphan")
    amenities = relationship('Amenity', secondary="place_amenities", back_populates='places')

    def __init__(self, title, price, latitude, longitude, owner_id, description=""):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.validate()

    def validate(self):
        if not isinstance(self.title, str) or len(self.title) > 100:
            raise ValueError("Title is too long or not a string")
        if not isinstance(self.price, (float, int)) or self.price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(self.latitude, (float, int)) or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Invalid latitude value")
        if not isinstance(self.longitude, (float, int)) or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Invalid longitude value")

    def __str__(self):
        return f"Place: {self.title} (Owner ID: {self.owner_id})"
