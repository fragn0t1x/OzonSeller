from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('ProductCategory', backref='products', foreign_keys=[category_id])

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def variations_count(self):
        from app.models import ProductVariation
        return ProductVariation.query.filter_by(product_id=self.id).count()


class ProductVariation(db.Model):
    __tablename__ = 'product_variations'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    sku = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    package_quantity = db.Column(db.Integer, default=1)
    variation_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generate_variation_name()

    def _generate_variation_name(self):
        """Генерация названия вариации"""
        parts = []
        if self.color:
            parts.append(f"Цвет {self.color}")
        if self.size:
            parts.append(f"Размер {self.size}")
        if self.package_quantity and self.package_quantity > 1:
            parts.append(f"{self.package_quantity} шт")
        self.variation_name = ", ".join(parts) if parts else "Базовая позиция"

    def __repr__(self):
        return f'<ProductVariation {self.sku} - {self.variation_name}>'

    def get_stock(self):
        """Получаем остатки через явный запрос"""
        from app.models import OurWarehouseStock
        from app import db

        stock = OurWarehouseStock.query.filter_by(variation_id=self.id).first()

        # Если остатков нет - создаем запись
        if not stock:
            stock = OurWarehouseStock(
                variation_id=self.id,
                unpacked_quantity=0,
                packed_quantity=0
            )
            db.session.add(stock)
            db.session.commit()

        return stock