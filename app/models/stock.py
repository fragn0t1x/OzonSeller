from app import db
from datetime import datetime


class StockUnpackaged(db.Model):
    __tablename__ = 'stock_unpackaged'

    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('product_variations.id', ondelete='CASCADE'), nullable=False,
                             unique=True)
    quantity_pieces = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    variation = db.relationship('ProductVariation', backref='stock')

    def __repr__(self):
        return f'<StockUnpackaged {self.quantity_pieces} шт.>'


class StockPackaged(db.Model):
    __tablename__ = 'stock_packaged'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('product_packages.id', ondelete='CASCADE'), nullable=False,
                           unique=True)
    quantity_packages = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    package = db.relationship('ProductPackage', backref='stock')

    def __repr__(self):
        return f'<StockPackaged {self.quantity_packages} уп.>'