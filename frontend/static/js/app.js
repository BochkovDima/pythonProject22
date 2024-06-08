document.getElementById('task-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const title = document.getElementById('task-title').value;
    const desc = document.getElementById('task-desc').value;

    const response = await fetch('/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, description: desc }),
    });

    if (response.ok) {
        document.getElementById('task-title').value = '';
        document.getElementById('task-desc').value = '';
    } else {
        console.error('Failed to add task');
    }
});