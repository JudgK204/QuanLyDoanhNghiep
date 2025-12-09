document.addEventListener("DOMContentLoaded", function () {
    const root = document.getElementById("tree-root");
    if (!root) return;

    loadChildren(1, root);

    const btn = document.getElementById("btnCreateFolder");
    if (btn) btn.addEventListener("click", submitCreateFolder);

    const cancelBtn = document.getElementById("btnCancelCreate");
    if (cancelBtn) cancelBtn.onclick = closeCreateModal;
});

// Hàm fetch JSON
function fetchJson(url, options) {
    return fetch(url, options).then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
    });
}

// Load thư mục con
function loadChildren(parentId, container) {
    fetchJson(`/api/folder/children/${parentId}`)
        .then(data => {
            const children = Array.isArray(data.children) ? data.children : [];
            container.innerHTML = "";

            const ul = document.createElement("ul");
            ul.classList.add("tree-root");

            children.forEach(item => {
                const li = document.createElement("li");
                li.setAttribute("data-id", item.ID);

                const span = document.createElement("span");
                span.textContent = item.Name;
                span.classList.add("tree-node", "caret");
                span.onclick = () => toggleNode(item.ID, li, span);

                // Nút thêm
                const addBtn = document.createElement("button");
                addBtn.textContent = "+";
                addBtn.classList.add("add-btn");
                addBtn.onclick = (e) => {
                    e.stopPropagation();
                    openCreateModal(item.ID, item.Level);
                };

                // Nút xóa
                const delBtn = document.createElement("button");
                delBtn.textContent = "-";
                delBtn.classList.add("delete-btn");
                delBtn.onclick = (e) => {
                    e.stopPropagation();
                    deleteFolder(item.ID, item.Name);
                };

                li.appendChild(span);
                li.appendChild(addBtn);
                li.appendChild(delBtn);
                ul.appendChild(li);
            });

            container.appendChild(ul);
        })
        .catch(err => {
            container.innerHTML = `<div class='error'>Lỗi: ${err.message}</div>`;
        });
}

// Toggle node
function toggleNode(nodeId, liElement, spanElement) {
    let childUl = liElement.querySelector(":scope > ul");

    // Nếu đã load con -> chỉ đóng/mở
    if (childUl) {
        const isOpen = childUl.style.display !== "none";

        if (isOpen) {
            childUl.style.display = "none";
            spanElement.classList.remove("caret-down");
        } else {
            childUl.style.display = "block";
            spanElement.classList.add("caret-down");
        }
        return;
    }

    // Nếu chưa load con -> fetch
    fetchJson(`/api/folder/children/${nodeId}`)
        .then(data => {
            const children = data.children || [];
            const ul = document.createElement("ul");

            // Mặc định hiển thị khi load lần đầu
            ul.style.display = "block";

            children.forEach(item => {
                const li = document.createElement("li");
                li.setAttribute("data-id", item.ID);

                const span = document.createElement("span");
                span.textContent = item.Name;
                span.classList.add("tree-node", "caret");
                span.onclick = () => toggleNode(item.ID, li, span);

                const addBtn = document.createElement("button");
                addBtn.textContent = "+";
                addBtn.classList.add("add-btn");
                addBtn.onclick = (e) => {
                    e.stopPropagation();
                    openCreateModal(item.ID, item.Level);
                };

                const delBtn = document.createElement("button");
                delBtn.textContent = "-";
                delBtn.classList.add("delete-btn");
                delBtn.onclick = (e) => {
                    e.stopPropagation();
                    deleteFolder(item.ID, item.Name);
                };

                li.appendChild(span);
                li.appendChild(addBtn);
                li.appendChild(delBtn);
                ul.appendChild(li);
            });

            liElement.appendChild(ul);
            spanElement.classList.add("caret-down");
        });
}


// Mở modal tạo thư mục
function openCreateModal(parentId, level) {
    const modal = document.getElementById("createFolderModal");
    if (!modal) {
        alert("Không tìm thấy modal tạo thư mục!");
        return;
    }

    document.getElementById("create_parent_id").value = parentId;
    document.getElementById("create_level").value = level;

    modal.classList.remove("hidden");
}

// Đóng modal
function closeCreateModal() {
    document.getElementById("createFolderModal").classList.add("hidden");
}

// Submit tạo thư mục – KHÔNG reload trang
function submitCreateFolder() {
    const parentId = Number(document.getElementById("create_parent_id").value);
    const level = Number(document.getElementById("create_level").value);
    const name = document.getElementById("newFolderName").value;
    const desc = document.getElementById("newFolderDesc").value;

    if (!name) return alert("Tên thư mục không được trống");

    fetchJson("/api/folder/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            parent_id: parentId,
            name: name,
            description: desc,
            level: level
        })
    })
        .then(() => {
            closeCreateModal();

            // Reload chính xác node cha (không ảnh hưởng các node khác)
            const parentLi = document.querySelector(`li[data-id='${parentId}']`);
            if (parentLi) {
                const childUl = parentLi.querySelector("ul");
                if (childUl) {
                    loadChildren(parentId, parentLi);
                }
            }

            alert("Tạo thư mục thành công!");
        })
        .catch(err => alert("Lỗi: " + err.message));
}

// Xóa thư mục
function deleteFolder(id, name) {
    if (!confirm(`Bạn có chắc muốn xóa thư mục "${name}"?\nToàn bộ thư mục con sẽ bị xóa.`)) return;

    fetchJson(`/api/folder/delete/${id}`, { method: "DELETE" })
        .then(() => {
            const li = document.querySelector(`li[data-id='${id}']`);
            if (li && li.parentNode) li.parentNode.removeChild(li);

            alert("Đã xóa thư mục!");
        })
        .catch(err => alert("Lỗi: " + err.message));
}
