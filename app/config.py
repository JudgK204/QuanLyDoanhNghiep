from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------
# CONFIG DATABASE
# ------------------------
DB_USER = "sa"
DB_PASSWORD = "12"
DB_NAME = "QLDNUD"
DB_SERVER = "JOY\ADMINISTRATOR"   # Nếu server khác, ví dụ 192.168.1.10 thì đổi tại đây

DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
print(">>> USING DATABASE:", DATABASE_URL) 
# ------------------------
# ENGINE + SESSION
# ------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,              # In câu SQL để debug, nếu không thích thì đặt False
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
