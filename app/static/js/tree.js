document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('tree-root-wrapper');
    const uploadModal = document.getElementById('uploadModal');
    const btnUpload = document.getElementById('btnUpload');
    const uploadForm = document.getElementById('uploadForm');
    const uploadNodeInput = document.getElementById('upload_node_id');
    const btnCancelUpload = document.getElementById('btnCancelUpload');
    const breadcrumbDiv = document.getElementById('breadcrumb');
    const btnBack = document.getElementById('btnBack');
    const fileListDiv = document.getElementById('fileList');

    let currentParent = null;
    let navStack = [];

    // load root columns (top-level)
    fetchColumn(null);

    btnUpload && btnUpload.addEventListener('click', () => {
        uploadNodeInput.value = '';
        openModal();
    });
    btnCancelUpload && btnCancelUpload.addEventListener('click', closeModal);

    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData(uploadForm);
            try {
                const res = await fetch('/api/upload/', { method: 'POST', body: fd });
                const j = await res.json();
                if (!res.ok) {
                    alert(j.error || JSON.stringify(j));
                    return;
                }
                alert('Uploaded');
                closeModal();
                loadFolder(currentParent);
            } catch (err) {
                console.error(err);
                alert('Upload failed');
            }
        });
    }

    function openModal(){ uploadModal.classList.remove('hidden'); }
    function closeModal(){ uploadModal.classList.add('hidden'); }

    uploadModal.addEventListener('click', (ev) => {
        if (ev.target === uploadModal) closeModal();
    });

    async function fetchColumn(parentId) {
        currentParent = parentId === null || parentId === '' ? null : parentId;
        const url = '/api/children/?parent_id=' + (parentId === null ? '' : parentId);
        try {
            const resp = await fetch(url);
            if (!resp.ok) { console.error('fetch failed', resp.status); return; }
            const data = await resp.json();
            renderColumn(parentId, data.children || []);
        } catch(err) {
            console.error('fetchColumn error', err);
        }
    }

    function renderColumn(parentId, children) {
        const cols = Array.from(wrapper.querySelectorAll('.tree-column'));
        let keepIndex = -1;
        if (parentId === null) keepIndex = -1;
        else keepIndex = cols.findIndex(c => c.dataset.parentId === String(parentId));
        for (let i = cols.length - 1; i > keepIndex; i--) cols[i].remove();

        const col = document.createElement('div');
        col.className = 'tree-column';
        col.dataset.parentId = parentId === null ? '' : String(parentId);

        if (!children.length) {
            const empty = document.createElement('div');
            empty.className = 'text-muted';
            empty.textContent = '(Không có mục con)';
            col.appendChild(empty);
        } else {
            children.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'tree-item';
                const left = document.createElement('div');
                left.innerHTML = `${item.Level && item.Level > 0 ? '📁' : '📄'} <span style="margin-left:8px">${escapeHtml(item.Name)}</span>`;
                const addBtn = document.createElement('button');
                addBtn.type = 'button';
                addBtn.textContent = '+';
                addBtn.className = 'add-btn';
                addBtn.style.marginRight = '10px';
                addBtn.onclick = (ev) => {
                    ev.stopPropagation();
                    openCreateModal(item.id, item.Level);
                };
                left.prepend(addBtn);
                itemDiv.appendChild(left);

                const right = document.createElement('div');
                // upload allowed for specific levels: 3,4,5,6,10,11 etc (adjust as needed)
                const uploadAllowedLevels = [3,4,5,6,10,11];
                if (uploadAllowedLevels.includes(item.Level)) {
                    const cloudBtn = document.createElement('button');
                    cloudBtn.type = 'button';
                    cloudBtn.className = 'upload-btn';
                    cloudBtn.style.border = 'none';
                    cloudBtn.style.background = 'transparent';
                    cloudBtn.style.cursor = 'pointer';
                    cloudBtn.textContent = '☁';
                    cloudBtn.title = 'Upload';
                    cloudBtn.dataset.nodeId = item.id;
                    cloudBtn.addEventListener('click', (ev) => {
                        ev.stopPropagation();
                        uploadNodeInput.value = item.id;
                        openModal();
                    });
                    right.appendChild(cloudBtn);
                }
                itemDiv.appendChild(right);

                itemDiv.addEventListener('click', () => loadFolder(item.id));
                col.appendChild(itemDiv);
            });
        }

        wrapper.appendChild(col);
        wrapper.scrollLeft = wrapper.scrollWidth;
    }

    function escapeHtml(s){
        if(s === null || s === undefined) return '';
        return String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]);
    }

    // -------- load node (children + files + breadcrumb)
    async function loadFolder(nodeId) {
        // nodeId may be null -> load top level
        if (!nodeId) {
            fetchColumn(null);
            breadcrumbDiv.innerText = "Home";
            navStack = [];
            updateBackButton();
            fileListDiv.innerHTML = "";
            return;
        }

        const res = await fetch(`/api/load-node/${nodeId}/`);
        if (!res.ok) { console.error('load node failed', res.status); return; }
        const data = await res.json();

        // render breadcrumb
        updateBreadcrumb(data.breadcrumb);

        // render files (if any)
        let html = `<h3>📁 ${escapeHtml(data.node.name)}</h3>`;
        if (data.children && data.children.length) {
            html += `<h4>Thư mục con</h4><ul>`;
            data.children.forEach(c => {
                html += `<li><a href="#" onclick="loadFolder(${c.id});return false;">${escapeHtml(c.name)}</a></li>`;
            });
            html += `</ul>`;
        } else {
            html += `<div>(Không có thư mục con)</div>`;
        }

        if (data.files && data.files.length) {
            html += `<h4>Danh sách file</h4><ul>`;
            data.files.forEach(f => {
                // file_path may be full path; use /media/{{node}}/name path pattern
                const url = `/media/${f.node_id}/${encodeURIComponent(f.file_name)}`;
                html += `<li><a href="${url}" target="_blank">${escapeHtml(f.file_name)}</a> <small>(${new Date(f.uploaded_at).toLocaleString()})</small></li>`;
            });
            html += `</ul>`;
        }

        fileListDiv.innerHTML = html;

        // append column for this node (so user can open next level)
        fetchColumn(nodeId);

        // push nav stack for back button
        if (navStack[navStack.length -1] !== nodeId) navStack.push(nodeId);
        updateBackButton();
        currentParent = nodeId;
    }

    function updateBreadcrumb(list) {
        if (!list || !list.length) {
            breadcrumbDiv.innerText = "Home";
            return;
        }
        let html = `<a href="#" data-id="">Home</a> / `;
        list.forEach((item, idx) => {
            if (idx === list.length - 1) html += `<span>${escapeHtml(item.name)}</span>`;
            else html += `<a href="#" data-id="${item.id}">${escapeHtml(item.name)}</a> / `;
        });
        breadcrumbDiv.innerHTML = html;

        breadcrumbDiv.querySelectorAll("a").forEach(a => {
            a.addEventListener("click", e => {
                e.preventDefault();
                const id = a.getAttribute("data-id") || null;
                navStack = [];
                loadFolder(id);
            });
        });
    }

    function updateBackButton() {
        btnBack.style.display = navStack.length > 1 ? "inline-block" : "none";
        btnBack.onclick = () => {
            navStack.pop();
            const prev = navStack[navStack.length -1] || null;
            loadFolder(prev);
        };
    }

    // make loadFolder global so template links can call it
    window.loadFolder = loadFolder;
});

// =============================
//  CREATE FOLDER (Thêm Quận/Phường)
// =============================

const createFolderModal = document.getElementById('createFolderModal');
const txtNewFolder = document.getElementById('newFolderName');
const txtNewDesc = document.getElementById('newFolderDesc');
const inputParent = document.getElementById('create_parent_id');
const inputLevel = document.getElementById('create_level');
const btnCreateFolder = document.getElementById('btnCreateFolder');
const btnCancelCreate = document.getElementById('btnCancelCreate');

function openCreateModal(parentId, level){
    inputParent.value = parentId;
    inputLevel.value = level + 1;
    txtNewFolder.value = "";
    txtNewDesc.value = "";
    createFolderModal.classList.remove("hidden");
}

function closeCreateModal(){
    createFolderModal.classList.add("hidden");
}

if (btnCancelCreate) {
    btnCancelCreate.onclick = closeCreateModal;
}

btnCreateFolder.onclick = async () => {
    const name = txtNewFolder.value.trim();
    if (!name) {
        alert("Tên thư mục không được để trống");
        return;
    }

    const body = {
        parent_id: Number(inputParent.value),
        name: name,
        description: txtNewDesc.value.trim(),
        level: Number(inputLevel.value)
    };


    const res = await fetch("/api/folder/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const j = await res.json();

    if (!res.ok) {
        alert(j.error || JSON.stringify(j));
        return;
    }

    alert("Tạo thư mục thành công");

    closeCreateModal();

    // Reload cột hiện tại để thấy folder mới
    fetchColumn(body.ParentID);
};

