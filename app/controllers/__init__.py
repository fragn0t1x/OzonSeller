from app.controllers.main import bp as main_bp
from app.controllers.products import bp as products_bp
from app.controllers.stocks import bp as stocks_bp
from app.controllers.categories import bp as categories_bp
from app.controllers.shipments import bp as shipments_bp

__all__ = ['main_bp', 'products_bp', 'stocks_bp', 'categories_bp', 'shipments_bp']