from flask import Blueprint, jsonify, request
from app.services.folder_service import (
    get_children,
    get_node,
    get_node_with_children_and_files,
    create_folder
)
from app.schemas.folder_schema import FolderSchema

from app.config.database import SessionLocal
from app.models import FolderTree

folder_router = Blueprint("folder", __name__)

# -----------------------
# GET: /children/<parent_id>
# -----------------------
@folder_router.get("/children/<int:parent_id>")
def api_get_children(parent_id):
    children = get_children(parent_id)
    data = [FolderSchema.model_validate(f).model_dump() for f in children]
    return jsonify({"children": data})

# -----------------------
# GET: /node/<node_id>
# -----------------------
@folder_router.get("/node/<int:node_id>")
def api_get_node(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "Not found"}), 404
    return jsonify(FolderSchema.model_validate(node).model_dump())

# -----------------------
# GET: /node_info/<node_id>
# -----------------------
@folder_router.get("/node_info/<int:node_id>")
def api_get_node_info(node_id):
    data = get_node_with_children_and_files(node_id)
    if not data:
        return jsonify({"error": "Not found"}), 404

    node = FolderSchema.model_validate(data["node"]).model_dump()
    children = [FolderSchema.model_validate(c).model_dump() for c in data["children"]]

    files = [
        {
            "ID": f.ID,
            "FolderID": f.FolderID,
            "FileName": f.FileName,
            "FilePath": f.FilePath,
        }
        for f in data["files"]
    ]

    return jsonify({
        "node": node,
        "children": children,
        "files": files
    })

# -----------------------
# POST: /create
# -----------------------
@folder_router.post("/create")
def api_create_folder():
    data = request.json or {}

    parent_id = data.get("parent_id")
    name = data.get("name")
    description = data.get("description")
    level = data.get("level")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        folder = create_folder(
            parent_id=parent_id,
            name=name,
            description=description,
            level=level
        )
        return jsonify({
            "ID": folder.ID,
            "ParentID": folder.ParentID,
            "Name": folder.Name,
            "Description": folder.Description,
            "Level": folder.Level
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# DELETE: /delete/<folder_id>
# -----------------------
@folder_router.delete("/delete/<int:folder_id>")
def api_delete_folder(folder_id):
    db = SessionLocal()

    folder = db.query(FolderTree).filter(FolderTree.ID == folder_id).first()
    if not folder:
        return jsonify({"error": "Folder not found"}), 404

    try:
        db.delete(folder)
        db.commit()
        return jsonify({"message": "Folder deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
