import re
import bcrypt
from .base_class import Baseclass

class User(Baseclass):
    """
    This class represents a user with secure password handling
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # This will be hashed
        self.is_admin = is_admin
        self._place = []

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
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) or len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password):
        """Verify if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode(), self._password.encode())

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

    def display(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }