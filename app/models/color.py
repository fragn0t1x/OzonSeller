from app import db
from datetime import datetime


class Color(db.Model):
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    hex_code = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Color {self.name}>'