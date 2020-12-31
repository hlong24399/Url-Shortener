from flask_sqlalchemy import SQLAlchemy
import datetime
from collections import deque
import math as m
db = SQLAlchemy()

ALPHABET_62= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String, unique=True, nullable=True)
    original_url = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        self.temp = self.created_at.strftime("%c")
        return f"{self.id} | {self.short_url} | {self.temp}"
