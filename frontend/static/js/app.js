console.log('app.js loaded');
document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');
    const pagination = document.getElementById('pagination');
    const tasksPerPage = 10;
    let currentPage = 1;
    let totalTasks = 0;

    function createTaskElement(task) {
        const row = document.createElement('tr');

        const checkboxCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = task.completed;
        checkbox.addEventListener('change', function() {
            fetch(`/tasks/${task.id}?completed=${this.checked}`, {
                method: 'PUT'
            }).then(response => {
                if (response.ok) {
                    row.classList.toggle('completed', this.checked);
                }
            });
        });
        checkboxCell.appendChild(checkbox);

        const titleCell = document.createElement('td');
        titleCell.textContent = task.title;

        const descCell = document.createElement('td');
        descCell.textContent = task.description;

        // Применение стиля, если задача выполнена
        if (task.completed) {
            titleCell.classList.add('completed');
            descCell.classList.add('completed');
        }

        const actionsCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', function() {
            fetch(`/tasks/${task.id}`, {
                method: 'DELETE'
            }).then(response => {
                if (response.ok) {
                    taskList.removeChild(row);
                    loadTasks();
                }
            });
        });
        actionsCell.appendChild(deleteButton);

        row.appendChild(checkboxCell);
        row.appendChild(titleCell);
        row.appendChild(descCell);
        row.appendChild(actionsCell);

        return row;
    }

    function loadTasks() {
        fetch(`/tasks?skip=${(currentPage - 1) * tasksPerPage}&limit=${tasksPerPage}`)
            .then(response => {
                totalTasks = parseInt(response.headers.get('X-Total-Count'), 10);
                console.log(`Total tasks from header: ${totalTasks}`);
                return response.json();
            })
            .then(data => {
                console.log('Tasks:', data);
                data.forEach(task => {
                    const taskElement = createTaskElement(task);
                    taskList.appendChild(taskElement);
                });
                renderPagination();
            });
    }

    function renderPagination() {
        console.log(`Rendering pagination with totalTasks: ${totalTasks}`);
        pagination.innerHTML = '';
        const totalPages = Math.ceil(totalTasks / tasksPerPage);
        console.log(`Total pages: ${totalPages}`);

        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            pageButton.disabled = (i === currentPage);
            pageButton.addEventListener('click', function() {
                currentPage = i;
                loadTasks();
            });
            pagination.appendChild(pageButton);
        }
    }

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('task-title').value;
        const description = document.getElementById('task-desc').value;
        const taskData = { title, description, completed: false };
        console.log('Submitting task:', taskData);
        fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        }).then(response => response.json())
          .then(task => {
              console.log('Task created:', task);
              const taskElement = createTaskElement(task);
              taskList.appendChild(taskElement);
              loadTasks();
              taskForm.reset();
          });
    });

    loadTasks();
    console.log('function: loadTasks() loaded';
});
