from sqlalchemy import Column, Integer, String, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime

class Files(Base):
    __tablename__ = "Files"

    ID = Column(Integer, primary_key=True)
    FolderID = Column(Integer, ForeignKey("FolderTree.ID"), nullable=False)
    FileName = Column(String(255), nullable=False)
    StoredName = Column(String(255), nullable=False)
    FileType = Column(String(50))
    FileSize = Column(BigInteger)
    UploadedAt = Column(DateTime, default=datetime.utcnow)
    Description = Column(Text)

    folder = relationship("FolderTree", back_populates="files")

    def to_dict(self):
        return {
            "ID": self.ID,
            "FolderID": self.FolderID,
            "FileName": self.FileName,
            "StoredName": self.StoredName,
            "FileType": self.FileType,
            "FileSize": self.FileSize,
            "UploadedAt": self.UploadedAt.isoformat(),
            "Description": self.Description
        }
