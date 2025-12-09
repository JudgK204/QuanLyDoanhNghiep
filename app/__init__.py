from flask import Flask
from app.config.config import Config

def create_app():
    app = Flask(__name__)

    # Load config trực tiếp từ class
    app.config.from_object(Config)

    # Khởi tạo DB và tạo bảng
    from app.config.database import init_db
    init_db()

    # Đăng ký blueprint
    from app.views import bp
    app.register_blueprint(bp)

    return app
