from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.models.base_class import Baseclass
from app import db

class Review(Baseclass):
    """
    Review class representing feedback left on a place.
    """
    __tablename__ = 'reviews'

    text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    @validates('text')
    def validate_text(self, key, value):
        """Ensures review text is not empty and within limits."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string")
        if len(value) > 500:
            raise ValueError("Review text must be 500 characters or fewer")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        """Ensures rating is between 1 and 5."""
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return value

    @validates('place_id')
    def validate_place_id(self, key, value):
        """Ensures place_id is a valid integer."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Invalid place ID")
        return value

    @validates('user_id')
    def validate_user_id(self, key, value):
        """Ensures user_id is a valid integer."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Invalid user ID")
        return value

    def to_dict(self):
        """Converts the Review object to a dictionary (excluding relationships)."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }

    def __str__(self):
        return (
            f'Review: (id={self.id}, text={self.text}, rating={self.rating}, '
            f'place_id={self.place_id}, user_id={self.user_id})'
        )
