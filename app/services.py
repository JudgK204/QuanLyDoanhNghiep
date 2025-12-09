from .config.init_db import SessionLocal
from .models import FolderTree, UploadedFile
from sqlalchemy import select
from sqlalchemy.orm import selectinload

def get_children(parent_id):
    db = SessionLocal()
    try:
        if parent_id in (None, "", 0, "0"):
            stmt = select(FolderTree).where(FolderTree.ParentID == None).order_by(FolderTree.ID)
        else:
            stmt = select(FolderTree).where(FolderTree.ParentID == int(parent_id)).order_by(FolderTree.ID)
        rows = db.execute(stmt).scalars().all()
        return [r.to_dict() for r in rows]
    finally:
        db.close()

def get_node(node_id):
    db = SessionLocal()
    try:
        n = db.get(FolderTree, int(node_id))
        return n
    finally:
        db.close()

def get_node_with_children_and_files(node_id):
    db = SessionLocal()
    try:
        stmt = select(FolderTree).options(selectinload(FolderTree.files), selectinload(FolderTree.children)).where(FolderTree.ID == int(node_id))
        res = db.execute(stmt).scalars().first()
        if not res:
            return None
        node = res
        children = [c.to_dict() for c in node.children]
        files = [f.to_dict() for f in node.files]
        return {"node": node.to_dict(), "children": children, "files": files}
    finally:
        db.close()

def get_breadcrumb(node):
    # returns list of ancestor dicts from root -> node
    res = []
    db = SessionLocal()
    try:
        cur = node
        while cur is not None:
            res.append(cur.to_dict())
            if cur.ParentID:
                cur = db.get(FolderTree, cur.ParentID)
            else:
                cur = None
        res.reverse()
        return res
    finally:
        db.close()

def save_upload(node_id, filename, filepath):
    db = SessionLocal()
    try:
        uf = UploadedFile(NodeID=int(node_id), FileName=filename, FilePath=filepath)
        db.add(uf)
        db.commit()
        db.refresh(uf)
        return uf.to_dict()
    finally:
        db.close()

def get_all_nodes():
    db = SessionLocal()
    try:
        stmt = select(FolderTree).order_by(FolderTree.ID)
        rows = db.execute(stmt).scalars().all()
        return [r.to_dict() for r in rows]
    finally:
        db.close()
