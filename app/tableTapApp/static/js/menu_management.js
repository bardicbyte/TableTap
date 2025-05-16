// Menu Management JS

document.addEventListener('DOMContentLoaded', function() {
    // Create Category Form Submission
    document.getElementById('createCategoryForm').onsubmit = function(e) {
        e.preventDefault();
        const menuId = document.getElementById('createCategoryMenuId').value;
        const name = document.getElementById('categoryName').value;
        fetch(`/api/menus/${menuId}/categories/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ name })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Hide the modal and remove any lingering backdrops
                bootstrap.Modal.getOrCreateInstance(document.getElementById('createCategoryModal')).hide();
                setTimeout(() => {
                    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                    document.body.classList.remove('modal-open');
                    window.openMenuDetail(menuId); // Refresh the modal content
                }, 300);
            } else {
                alert('Error: ' + (data.error || 'Could not create category.'));
            }
        });
    };

    // Edit Category Form Submission
    document.getElementById('editCategoryForm').onsubmit = function(e) {
        e.preventDefault();
        const catId = document.getElementById('editCategoryId').value;
        const menuId = document.getElementById('editCategoryMenuId').value;
        const name = document.getElementById('editCategoryName').value;
        fetch(`/api/categories/${catId}/edit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ name })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                bootstrap.Modal.getOrCreateInstance(document.getElementById('editCategoryModal')).hide();
                window.openMenuDetail(menuId); // Refresh the modal content
            } else {
                alert('Error: ' + (data.error || 'Could not update category.'));
            }
        });
    };

    // Item Form Submission
    document.getElementById('itemForm').onsubmit = function(e) {
        e.preventDefault();
        const itemId = document.getElementById('itemId').value;
        const catId = document.getElementById('itemCategoryId').value;
        const name = document.getElementById('itemName').value;
        const description = document.getElementById('itemDescription').value;
        const price = document.getElementById('itemPrice').value;
        const image_url = document.getElementById('itemImageUrl').value;
        const url = itemId ? `/api/items/${itemId}/edit/` : `/api/categories/${catId}/items/create/`;
        const method = 'POST';
        fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ name, description, price, image_url })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                bootstrap.Modal.getOrCreateInstance(document.getElementById('itemModal')).hide();
                // Refresh the menu detail modal
                const menuId = document.getElementById('menuDetailContent').querySelector('button.btn-primary').getAttribute('onclick').match(/\d+/)[0];
                window.openMenuDetail(menuId);
            } else {
                alert('Error: ' + (data.error || 'Could not save item.'));
            }
        });
    };
});

// Functions called from HTML (onclick, etc.)
window.editMenu = function(menuId) {
    // Fetch menu data and populate the edit form
    fetch(`/api/menus/${menuId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editMenuName').value = data.name;
            document.getElementById('editMenuDescription').value = data.description;
            document.getElementById('editMenuActive').checked = data.is_active;
            document.getElementById('editMenuForm').action = `/api/menus/${menuId}/update/`;
            new bootstrap.Modal(document.getElementById('editMenuModal')).show();
        });
};

window.deleteMenu = function(menuId) {
    if (confirm('Are you sure you want to delete this menu?')) {
        fetch(`/api/menus/${menuId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    }
};

window.openMenuDetail = function(menuId) {
    // Fetch categories and items for this menu via AJAX
    fetch(`/api/menus/${menuId}/detail/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('menuDetailTitle').innerText = data.menu.name + ' - Categories & Items';
            let html = '';
            html += `<button class='btn btn-primary mb-3' onclick='showCreateCategoryModal(${menuId})'><i class='fas fa-plus'></i> Add Category</button>`;
            if (data.categories.length === 0) {
                html += `<div class='alert alert-info'>No categories yet. Add your first category!</div>`;
            }
            data.categories.forEach(cat => {
                html += `<div class='card mb-3'>
                    <div class='card-header d-flex justify-content-between align-items-center'>
                        <span><b>${cat.name}</b></span>
                        <div>
                            <button class='btn btn-sm btn-outline-primary' onclick='showEditCategoryModal(${cat.id}, \"${cat.name}\", event)'><i class='fas fa-edit'></i></button>
                            <button class='btn btn-sm btn-outline-danger' onclick='deleteCategory(${cat.id}, ${menuId}, event)'><i class='fas fa-trash'></i></button>
                            <button class='btn btn-sm btn-success ms-2' onclick='showCreateItemModal(${cat.id}, event)'><i class='fas fa-plus'></i> Add Item</button>
                        </div>
                    </div>
                    <ul class='list-group list-group-flush'>`;
                if (cat.items.length === 0) {
                    html += `<li class='list-group-item text-muted'>No items in this category.</li>`;
                }
                cat.items.forEach(item => {
                    html += `<li class='list-group-item d-flex justify-content-between align-items-center'>
                        <div>
                            <b>${item.name}</b> - $${item.price} <br><small>${item.description}</small>
                        </div>
                        <div>
                            <button class='btn btn-sm btn-outline-primary' onclick='showEditItemModal(${item.id}, event)'><i class='fas fa-edit'></i></button>
                            <button class='btn btn-sm btn-outline-danger' onclick='deleteItem(${item.id}, ${cat.id}, event)'><i class='fas fa-trash'></i></button>
                        </div>
                    </li>`;
                });
                html += `</ul></div>`;
            });
            document.getElementById('menuDetailContent').innerHTML = html;
            new bootstrap.Modal(document.getElementById('menuDetailModal')).show();
        });
};

window.showCreateCategoryModal = function(menuId) {
    document.getElementById('createCategoryMenuId').value = menuId;
    document.getElementById('categoryName').value = '';
    new bootstrap.Modal(document.getElementById('createCategoryModal')).show();
};

window.showEditCategoryModal = function(catId, catName, event) {
    event.stopPropagation();
    document.getElementById('editCategoryId').value = catId;
    document.getElementById('editCategoryName').value = catName;
    // Find the menuId from the currently open menu detail modal
    const menuId = document.getElementById('menuDetailContent').querySelector('button.btn-primary').getAttribute('onclick').match(/\d+/)[0];
    document.getElementById('editCategoryMenuId').value = menuId;
    new bootstrap.Modal(document.getElementById('editCategoryModal')).show();
};

window.deleteCategory = function(catId, menuId, event) {
    event.stopPropagation();
    if(confirm('Delete this category?')) {
        fetch(`/api/categories/${catId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.openMenuDetail(menuId); // Refresh the modal content
            } else {
                alert('Error: ' + (data.error || 'Could not delete category.'));
            }
        });
    }
};

window.showCreateItemModal = function(catId, event) {
    event.stopPropagation();
    document.getElementById('itemModalTitle').innerText = 'Add Item';
    document.getElementById('itemModalSubmit').innerText = 'Add Item';
    document.getElementById('itemId').value = '';
    document.getElementById('itemCategoryId').value = catId;
    document.getElementById('itemName').value = '';
    document.getElementById('itemDescription').value = '';
    document.getElementById('itemPrice').value = '';
    document.getElementById('itemImageUrl').value = '';
    new bootstrap.Modal(document.getElementById('itemModal')).show();
};

window.showEditItemModal = function(itemId, event) {
    event.stopPropagation();
    fetch(`/api/items/${itemId}/`) // Get item details
        .then(response => response.json())
        .then(data => {
            document.getElementById('itemModalTitle').innerText = 'Edit Item';
            document.getElementById('itemModalSubmit').innerText = 'Save Changes';
            document.getElementById('itemId').value = data.id;
            document.getElementById('itemCategoryId').value = data.menu_category;
            document.getElementById('itemName').value = data.name;
            document.getElementById('itemDescription').value = data.description;
            document.getElementById('itemPrice').value = data.price;
            document.getElementById('itemImageUrl').value = data.image_url;
            new bootstrap.Modal(document.getElementById('itemModal')).show();
        });
};

window.deleteItem = function(itemId, catId, event) {
    event.stopPropagation();
    if(confirm('Delete this item?')) {
        fetch(`/api/items/${itemId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Refresh the menu detail modal
                const menuId = document.getElementById('menuDetailContent').querySelector('button.btn-primary').getAttribute('onclick').match(/\d+/)[0];
                window.openMenuDetail(menuId);
            } else {
                alert('Error: ' + (data.error || 'Could not delete item.'));
            }
        });
    }
};

window.showQrModal = function(menuId, menuName) {
    const link = `${window.location.origin}/menu/${menuId}/view/`;
    document.getElementById('qrModalTitle').innerText = `${menuName} - QR Code`;
    document.getElementById('qrImage').src = `/menu/${menuId}/qr/`;
    document.getElementById('qrMenuLink').value = link;
    new bootstrap.Modal(document.getElementById('qrModal')).show();
};

window.copyQrLink = function() {
    const input = document.getElementById('qrMenuLink');
    input.select();
    input.setSelectionRange(0, 99999);
    document.execCommand('copy');
};
