import os

class Config:
    SECRET_KEY = "your-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///seed.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
