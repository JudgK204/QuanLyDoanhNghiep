import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Lấy DB URL từ biến môi trường hoặc fallback sang SQL Server
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mssql+pyodbc://JOY\\ADMINISTRATOR:123@LOCALHOST/QLDNUD?driver=ODBC+Driver+17+for+SQL+Server"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
