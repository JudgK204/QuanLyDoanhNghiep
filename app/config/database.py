import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ========================
#  SQL SERVER CONNECTION
# ========================

DRIVER = "ODBC Driver 17 for SQL Server"

SERVER = r"JOY\ADMINISTRATOR"   # hoặc "localhost"
DATABASE = "QLDNUD"
USERNAME = "sa"
PASSWORD = "12"

connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "TrustServerCertificate=yes;"
)

connection_url = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(connection_string)

# ========================
#  SQLALCHEMY OBJECTS
# ========================

engine = create_engine(connection_url, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ========================
#  INIT DATABASE
# ========================
def init_db():
    """
    Khởi tạo bảng theo model (nếu chưa có)
    """
    import app.models.folder_tree  # load model
    Base.metadata.create_all(bind=engine)
