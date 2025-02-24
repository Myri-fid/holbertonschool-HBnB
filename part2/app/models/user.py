#!/usr/bin/python3
"""
This file provide an user class
"""
Base_class = __import__("base_class").Baseclass

class User(Base_class):
    """
    This class represent an user
    """
    def __init__(self, first_name, last_name, email, is_admin):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


user1 = User("Hilliass", "Soumahill", "Hilliass@mail.com", False)

print(user1.created_at)
