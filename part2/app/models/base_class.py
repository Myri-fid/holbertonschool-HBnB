#!/usr/bin/python3
"""
This file provides attribute and methods accessible 
bay other class 
"""
import uuid
from datetime import datetime

class Baseclass:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
