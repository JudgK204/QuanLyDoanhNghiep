from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class FolderTree(Base):
    __tablename__ = "folder"   # đúng theo bảng thực tế của bạn

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ParentID = Column(Integer, ForeignKey("folder.ID"), nullable=True)
    Name = Column(String(255), nullable=False)
    Level = Column(Integer, nullable=True)   # bảng thật có NULL
    Description = Column(Text, nullable=True)

    # Quan hệ cha-con
    children = relationship(
        "FolderTree",
        backref="parent",
        cascade="all, delete-orphan",
        lazy="joined",
        join_depth=5
    )

    def to_dict(self):
        return {
            "ID": self.ID,
            "ParentID": self.ParentID,
            "Name": self.Name,
            "Level": self.Level,
            "Description": self.Description
        }


class Files(Base):
    __tablename__ = "files"   # sửa cho đúng bảng lưu file (nếu khác bạn báo lại)

    ID = Column(Integer, primary_key=True, autoincrement=True)
    FolderID = Column(Integer, ForeignKey("folder.ID"), nullable=False)
    FileName = Column(String(255), nullable=False)
    StoredName = Column(String(255), nullable=False)
    FileType = Column(String(50))
    FileSize = Column(BigInteger)
    UploadedAt = Column(DateTime, default=datetime.utcnow)
    Description = Column(Text)

    folder = relationship("FolderTree", backref="files")

    def to_dict(self):
        return {
            "ID": self.ID,
            "FolderID": self.FolderID,
            "FileName": self.FileName,
            "StoredName": self.StoredName,
            "FileType": self.FileType,
            "FileSize": self.FileSize,
            "UploadedAt": self.UploadedAt.isoformat() if self.UploadedAt else None,
            "Description": self.Description
        }
