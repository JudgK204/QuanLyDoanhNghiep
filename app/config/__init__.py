from .database import Base, engine, SessionLocal
from .config import Config

def init_db():
    # Import tất cả models ở đây để SQLAlchemy nhận diện bảng
    from app.models import FolderTree, Files

    # Tạo bảng nếu chưa có
    Base.metadata.create_all(bind=engine)
