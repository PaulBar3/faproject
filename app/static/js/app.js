const API_BASE = '/api/v1';
let currentFilter = 'all';
let todos = [];

// Загрузка задач при старте
document.addEventListener('DOMContentLoaded', loadTodos);

// Обработчик формы
document.getElementById('todoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('titleInput').value.trim();
    const description = document.getElementById('descriptionInput').value.trim();
    
    if (!title) return;
    
    await createTodo({ title, description });
    document.getElementById('titleInput').value = '';
    document.getElementById('descriptionInput').value = '';
});

// Фильтры
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        renderTodos();
    });
});

// Сохранение редактирования
document.getElementById('saveEditBtn').addEventListener('click', async () => {
    const id = parseInt(document.getElementById('editId').value);
    const title = document.getElementById('editTitle').value.trim();
    const description = document.getElementById('editDescription').value.trim();
    const completed = document.getElementById('editCompleted').checked;
    
    if (!title) return;
    
    await updateTodo(id, { title, description, completed });
    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
});

async function loadTodos() {
    try {
        const response = await fetch(`${API_BASE}/todos`);
        todos = await response.json();
        renderTodos();
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        document.getElementById('todoList').innerHTML = `
            <div class="empty-state">
                <i class="bi bi-exclamation-triangle"></i>
                <p>Ошибка загрузки задач</p>
            </div>
        `;
    }
}

async function createTodo(todo) {
    try {
        const response = await fetch(`${API_BASE}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todo)
        });
        if (response.ok) {
            await loadTodos();
        }
    } catch (error) {
        console.error('Ошибка создания:', error);
    }
}

async function updateTodo(id, updates) {
    try {
        const response = await fetch(`${API_BASE}/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (response.ok) {
            await loadTodos();
        }
    } catch (error) {
        console.error('Ошибка обновления:', error);
    }
}

async function toggleTodo(id, completed) {
    await updateTodo(id, { completed: !completed });
}

async function deleteTodo(id) {
    if (!confirm('Удалить эту задачу?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/todos/${id}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            await loadTodos();
        }
    } catch (error) {
        console.error('Ошибка удаления:', error);
    }
}

function openEditModal(todo) {
    document.getElementById('editId').value = todo.id;
    document.getElementById('editTitle').value = todo.title;
    document.getElementById('editDescription').value = todo.description || '';
    document.getElementById('editCompleted').checked = todo.completed;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

function renderTodos() {
    let filtered = todos;
    
    if (currentFilter === 'active') {
        filtered = todos.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        filtered = todos.filter(t => t.completed);
    }
    
    if (filtered.length === 0) {
        document.getElementById('todoList').innerHTML = `
            <div class="empty-state">
                <i class="bi bi-clipboard-check"></i>
                <p>${currentFilter === 'all' ? 'Нет задач. Добавьте первую!' : 'Нет задач в этой категории'}</p>
            </div>
        `;
        return;
    }
    
    document.getElementById('todoList').innerHTML = filtered.map(todo => `
        <div class="card todo-item ${todo.completed ? 'completed' : ''}">
            <div class="card-body">
                <div class="d-flex align-items-center justify-content-between">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center gap-2 mb-1">
                            <input type="checkbox" class="form-check-input" 
                                   ${todo.completed ? 'checked' : ''}
                                   onchange="toggleTodo(${todo.id}, ${todo.completed})">
                            <span class="todo-title">${escapeHtml(todo.title)}</span>
                            <span class="badge ${todo.completed ? 'bg-success' : 'bg-primary'} badge-status">
                                ${todo.completed ? '✓ Готово' : '○ В процессе'}
                            </span>
                        </div>
                        ${todo.description ? `<p class="todo-description mb-0 ms-4">${escapeHtml(todo.description)}</p>` : ''}
                    </div>
                    <div class="todo-actions">
                        <button class="btn btn-outline-primary btn-sm" onclick="openEditModal(todos.find(t => t.id === ${todo.id}))">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger btn-sm" onclick="deleteTodo(${todo.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
