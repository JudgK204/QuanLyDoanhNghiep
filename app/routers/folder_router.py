from flask import Blueprint, jsonify
from app.services.folder_service import get_children, get_node, get_node_with_children_and_files
from app.schemas.folder_schema import FolderSchema

folder_router = Blueprint("folder", __name__)

# -----------------------
# GET: /api/folder/children/<parent_id>
# -----------------------
@folder_router.get("/api/folder/children/<int:parent_id>")
def api_get_children(parent_id):
    children = get_children(parent_id)
    data = [FolderSchema.model_validate(f).model_dump() for f in children]
    return jsonify(data)


# -----------------------
# GET: /api/folder/node/<node_id>
# -----------------------
@folder_router.get("/api/folder/node/<int:node_id>")
def api_get_node(node_id):
    node = get_node(node_id)
    if not node:
        return jsonify({"error": "Not found"}), 404
    return jsonify(FolderSchema.model_validate(node).model_dump())


# -----------------------
# GET: /api/folder/node_info/<node_id>
# -----------------------
@folder_router.get("/api/folder/node_info/<int:node_id>")
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
# POST: /api/folder/create
# -----------------------
@folder_router.post("/api/folder/create")
def api_create_folder():
    from flask import request

    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    parent_id = data.get("ParentID")
    name = data.get("Name")
    description = data.get("Description")
    level = data.get("Level")

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
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
