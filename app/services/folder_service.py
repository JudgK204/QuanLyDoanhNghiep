from app.config.database import SessionLocal
from app.models.folder_tree import FolderTree
from app.models.files import Files


# ============================
# 1. Tạo folder mới
# ============================
def create_folder(parent_id, name, description=None):
    db = SessionLocal()
    try:
        folder = FolderTree(
            ParentID=parent_id,
            Name=name,
            Description=description,
            Level=1,
        )
        db.add(folder)
        db.commit()
        db.refresh(folder)
        return folder
    finally:
        db.close()


# ============================
# 2. Lấy toàn bộ thư mục con
# ============================
def get_children(parent_id: int):
    db = SessionLocal()
    try:
        children = (
            db.query(FolderTree)
            .filter(FolderTree.ParentID == parent_id)
            .order_by(FolderTree.ID.asc())
            .all()
        )
        return children
    finally:
        db.close()


# ============================
# 3. Lấy node theo ID
# ============================
def get_node(node_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(FolderTree)
            .filter(FolderTree.ID == node_id)
            .first()
        )
    finally:
        db.close()


# ============================
# 4. Node + children + file
# ============================
def get_node_with_children_and_files(node_id: int):
    db = SessionLocal()
    try:
        node = (
            db.query(FolderTree)
            .filter(FolderTree.ID == node_id)
            .first()
        )
        if not node:
            return None

        children = (
            db.query(FolderTree)
            .filter(FolderTree.ParentID == node_id)
            .order_by(FolderTree.ID.asc())
            .all()
        )

        files = (
            db.query(Files)
            .filter(Files.FolderID == node_id)
            .all()
        )

        return {
            "node": node,
            "children": children,
            "files": files
        }
    finally:
        db.close()


# ============================
# 5. breadcrumb
# ============================
def get_breadcrumb(node_id: int):
    db = SessionLocal()
    try:
        path = []
        current = (
            db.query(FolderTree)
            .filter(FolderTree.ID == node_id)
            .first()
        )

        while current:
            path.append(current)
            if current.ParentID:
                current = (
                    db.query(FolderTree)
                    .filter(FolderTree.ID == current.ParentID)
                    .first()
                )
            else:
                current = None

        return path[::-1]
    finally:
        db.close()


# ============================
# 6. Lưu file
# ============================
def save_upload(folder_id, filename, filepath):
    db = SessionLocal()
    try:
        f = Files(
            FolderID=folder_id,
            FileName=filename,
            FilePath=filepath,
        )
        db.add(f)
        db.commit()
        db.refresh(f)
        return f
    finally:
        db.close()
