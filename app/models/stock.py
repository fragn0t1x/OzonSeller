from app import db
from datetime import datetime

class OurWarehouseStock(db.Model):
    __tablename__ = 'our_warehouse_stocks'

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), unique=True, nullable=False)
    unpacked_quantity = db.Column(db.Integer, default=0)
    packed_quantity = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<OurWarehouseStock {self.variation_id}>'

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StockMovement {self.movement_type} {self.quantity}>'