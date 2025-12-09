from flask import Blueprint, request, jsonify, render_template
from app.services.folder_service import (
    get_children,
    get_node,
    get_node_with_children_and_files,
    get_breadcrumb,
    create_folder,
    save_upload
)
from app.schemas.folder_schema import FolderSchema

bp = Blueprint("main", __name__)

# -----------------------
# Home page
# -----------------------
@bp.route("/")
def home():
    return render_template("folder_tree.html")


# -----------------------
# GET node + children + files
# -----------------------
@bp.route("/api/folder/node/<int:node_id>", methods=["GET"])
def api_node(node_id):
    data = get_node_with_children_and_files(node_id)
    if not data:
        return jsonify({"error": "Not found"}), 404

    node = FolderSchema.model_validate(data["node"]).model_dump()
    children = [
        FolderSchema.model_validate(c).model_dump()
        for c in data["children"]
    ]

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
# Breadcrumb
# -----------------------
@bp.route("/api/folder/breadcrumb/<int:node_id>", methods=["GET"])
def api_breadcrumb(node_id):
    path = get_breadcrumb(node_id)
    breadcrumb = [
        FolderSchema.model_validate(p).model_dump()
        for p in path
    ]
    return jsonify(breadcrumb)


# -----------------------
# Create folder
# -----------------------
@bp.route("/api/folder/create", methods=["POST"])
def api_create_folder():
    data = request.json

    folder = create_folder(
        parent_id=data["parent_id"],
        name=data["name"],
        description=data.get("description")
    )

    return jsonify(FolderSchema.model_validate(folder).model_dump())


# -----------------------
# File upload
# -----------------------
@bp.route("/api/file/upload", methods=["POST"])
def api_upload_file():
    file = request.files["file"]
    folder_id = int(request.form["folder_id"])
    description = request.form.get("description")

    saved = save_upload(folder_id, file.filename, description)
    return jsonify({
        "ID": saved.ID,
        "FolderID": saved.FolderID,
        "FileName": saved.FileName,
        "FilePath": saved.FilePath,
    })


# -----------------------
# GET children
# -----------------------
@bp.route("/api/folder/children/<int:parent_id>")
def api_get_children(parent_id):
    children = get_children(parent_id)
    serialized = [
        FolderSchema.model_validate(c).model_dump()
        for c in children
    ]
    return jsonify({"children": serialized})
