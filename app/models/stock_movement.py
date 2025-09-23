# app/models/stock_movement.py
from app import db
from datetime import datetime

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    movement_type = db.Column(db.String(50), nullable=False)  # 'incoming', 'packing'
    quantity = db.Column(db.Integer, nullable=False)
    package_quantity = db.Column(db.Integer, default=1)  # Для упаковок
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StockMovement {self.movement_type} {self.quantity}>'