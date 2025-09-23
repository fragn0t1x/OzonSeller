# app/models/shipment.py
from app import db
from datetime import datetime

class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    shipment_number = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, preparing, sent, delivered
    shipment_date = db.Column(db.DateTime)
    expected_delivery_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('ShipmentItem', backref='shipment', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Shipment {self.shipment_number}>'

class ShipmentItem(db.Model):
    __tablename__ = 'shipment_items'

    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id', ondelete='CASCADE'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('product_packages.id', ondelete='CASCADE'), nullable=False)  # Меняем на package_id
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    package = db.relationship('ProductPackage', backref='shipment_items')

    __table_args__ = (
        db.UniqueConstraint('shipment_id', 'package_id', name='_shipment_package_uc'),
    )

    def __repr__(self):
        return f'<ShipmentItem {self.quantity}>'