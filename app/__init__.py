# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


# app/__init__.py
def get_color_hex(color_name):
    """Функция для получения HEX кода цвета по названию"""
    if not color_name:
        return '#6c757d'

    color_name_lower = color_name.lower().strip()
    color_map = {
        'черный': '#000000',
        'белый': '#ffffff',
        'красный': '#dc3545',
        'синий': '#0d6efd',
        'зеленый': '#198754',
        'желтый': '#ffc107',
        'оранжевый': '#fd7e14',
        'фиолетовый': '#6f42c1',
        'розовый': '#e83e8c',
        'бирюзовый': '#20c997',
        'голубой': '#0dcaf0',
        'коричневый': '#795548',
        'серый': '#6c757d',
        # ДОБАВЛЯЕМ НОВЫЕ ЦВЕТА
        'разноцветный': '#ff6b6b',  # Яркий коралловый для разноцветного
        'светло-серый': '#adb5bd',  # Более светлый серый
        'темно-синий': '#1e40af'  # Темный синий
    }
    return color_map.get(color_name_lower, '#6c757d')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Добавляем функцию в контекст шаблонов
    app.jinja_env.globals['get_color_hex'] = get_color_hex

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация blueprint'ов
    from app.controllers.main import bp as main_bp
    from app.controllers.products import bp as products_bp
    from app.controllers.categories import bp as categories_bp
    from app.controllers.shipments import bp as shipments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(shipments_bp, url_prefix='/shipments')

    return app
