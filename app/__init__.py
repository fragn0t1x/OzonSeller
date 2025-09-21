from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация blueprint'ов
    from app.controllers.main import bp as main_bp
    from app.controllers.products import bp as products_bp
    from app.controllers.stocks import bp as stocks_bp
    from app.controllers.categories import bp as categories_bp
    from app.controllers.shipments import bp as shipments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(stocks_bp, url_prefix='/stocks')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(shipments_bp, url_prefix='/shipments')

    return app