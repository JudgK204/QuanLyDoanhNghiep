from pydantic import BaseModel

class FolderSchema(BaseModel):
    ID: int
    ParentID: int | None
    Name: str
    Description: str | None = None
    Level: int | None = None

    class Config:
        from_attributes = True
