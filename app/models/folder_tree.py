from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class FolderTree(Base):
    __tablename__ = "FolderTree"

    ID = Column(Integer, primary_key=True)
    ParentID = Column(Integer, ForeignKey("FolderTree.ID"), nullable=True)
    Name = Column(String(255), nullable=False)
    Level = Column(Integer, nullable=False)
    Description = Column(Text, nullable=True)

    parent = relationship("FolderTree", remote_side=[ID], backref="children")
    files = relationship("Files", back_populates="folder")

    def to_dict(self):
        return {
            "ID": self.ID,
            "ParentID": self.ParentID,
            "Name": self.Name,
            "Level": self.Level,
            "Description": self.Description
        }
