# config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///warehouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OZON API credentials
    OZON_CLIENT_ID = os.environ.get('OZON_CLIENT_ID')
    OZON_API_KEY = os.environ.get('OZON_API_KEY')

    # Pagination
    ITEMS_PER_PAGE = 20