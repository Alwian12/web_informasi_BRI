import os
import socket

from dotenv import load_dotenv

load_dotenv()


def _resolve_database_url():
    db_url = os.getenv('DATABASE_URL')

    if not db_url:
        return 'sqlite:///db_pelayanan_perbankan.db'

    if db_url.startswith('mysql'):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect(('localhost', 3306))
        except OSError:
            return 'sqlite:///db_pelayanan_perbankan.db'

    return db_url


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')
    SQLALCHEMY_DATABASE_URI = _resolve_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAIL_SERVER = os.getenv('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in {'1', 'true', 'yes', 'on'}
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'lupirpl234@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') or MAIL_USERNAME
