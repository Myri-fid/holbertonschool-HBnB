#!/usr/bin/python3
"""
This file provide an user class
"""
import re
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
        self.place = []

    @property
    def get_first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if re.match(r"^[A-Z][a-z]+$", value, re.UNICODE) is not None:
            self._first_name = value
        else:
            raise ValueError("Wrong input !")
