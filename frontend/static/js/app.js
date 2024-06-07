async function fetchTasks() {
    try {
        const response = await fetch('/tasks');
        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }
        const tasks = await response.json();
        console.log('Fetched tasks:', tasks);  // Добавьте это для логирования
        const taskList = document.getElementById('task-list');
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';

            const taskTitle = document.createElement('span');
            taskTitle.className = 'task-title';
            taskTitle.innerText = task.title;

            const taskDesc = document.createElement('span');
            taskDesc.className = 'task-desc';
            taskDesc.innerText = task.description;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = task.completed;
            checkbox.onchange = () => deleteTask(task.id);

            taskItem.appendChild(checkbox);
            taskItem.appendChild(taskTitle);
            taskItem.appendChild(taskDesc);

            taskList.appendChild(taskItem);
        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

async function deleteTask(taskId) {
    try {
        console.log(`Deleting task id ${taskId}`);
        await fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        fetchTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}

async function addTask(event) {
    event.preventDefault();
    console.log('Adding task');
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-desc').value;

    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: title, description: description }),
        });

        if (!response.ok) {
            throw new Error('Failed to add task');
        }

        console.log('Task added successfully');
        document.getElementById('task-form').reset();
        fetchTasks();
    } catch (error) {
        console.error('Error adding task:', error);
    }
}

window.onload = () => {
    console.log('Window loaded');
    fetchTasks();
    const form = document.getElementById('task-form');
    form.onsubmit = addTask;
};