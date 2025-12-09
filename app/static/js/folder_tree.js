document.addEventListener("DOMContentLoaded", function () {
    const root = document.getElementById("tree-root");
    if (!root) return;

    loadChildren(1, root);
});

function fetchJson(url) {
    return fetch(url).then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
    });
}

function loadChildren(parentId, container) {
    fetchJson(`/api/folder/children/${parentId}`)
        .then(data => {
            const children = Array.isArray(data.children) ? data.children : [];

            container.innerHTML = "";

            if (children.length === 0) {
                container.innerHTML = "<div class='no-child'>Không có thư mục con</div>";
                return;
            }

            const ul = document.createElement("ul");
            ul.classList.add("tree-root");

            children.forEach(item => {
                const li = document.createElement("li");
                const span = document.createElement("span");

                span.textContent = item.Name;
                span.classList.add("tree-node", "caret");

                span.onclick = () => toggleNode(item.ID, li, span);

                li.appendChild(span);
                ul.appendChild(li);
            });

            container.appendChild(ul);
        })
        .catch(err => {
            container.innerHTML = `<div class='error'>Lỗi tải: ${err.message}</div>`;
        });
}

function toggleNode(nodeId, liElement, spanElement) {
    const existing = liElement.querySelector(":scope > ul");

    if (existing) {
        existing.classList.toggle("active");
        spanElement.classList.toggle("caret-down");
        return;
    }

    fetchJson(`/api/folder/children/${nodeId}`)
        .then(data => {
            const children = Array.isArray(data.children) ? data.children : [];

            const ul = document.createElement("ul");

            if (children.length === 0) {
                const note = document.createElement("div");
                note.classList.add("no-child");
                note.textContent = "(Không có mục con)";
                liElement.appendChild(note);
                return;
            }

            children.forEach(item => {
                const li = document.createElement("li");
                const span = document.createElement("span");

                span.textContent = item.Name;
                span.classList.add("tree-node", "caret");

                span.onclick = () => toggleNode(item.ID, li, span);

                li.appendChild(span);
                ul.appendChild(li);
            });

            ul.classList.add("active");
            spanElement.classList.add("caret-down");
            liElement.appendChild(ul);
        })
        .catch(err => {
            const note = document.createElement("div");
            note.classList.add("error");
            note.textContent = `Lỗi tải: ${err.message}`;
            liElement.appendChild(note);
        });
}
