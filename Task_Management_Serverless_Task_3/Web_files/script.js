endpoint = "YOUR-API-ENDPOINT"

document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');
    const tasksContainer = document.getElementById('tasksContainer');
    const messageContainer = document.getElementById('messageContainer');
    let currentTasks = [];

    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (currentTasks.length >= 8) {
            showMessage('Task limit reached. Cannot create more than 8 tasks.');
            return;
        }

        const taskName = document.getElementById('taskName').value;
        const taskDescription = document.getElementById('taskDescription').value;

        const taskId = getNewTaskId();

        const taskData = {
            taskId,
            taskName,
            taskDescription
        };

        toggleButtons(true);

        try {
            const response = await fetch(`${endpoint}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
            const result = await response.json();
            showMessage(result.body.replaceAll('"', ''));

            loadTasks();
        } catch (error) {
            console.error('Error creating task:', error);
        } finally {
            toggleButtons(false);
            taskForm.reset();
        }
    });

    async function loadTasks() {
        tasksContainer.innerHTML = '';
        try {
            const response = await fetch(`${endpoint}/tasks`);
            const result = await response.json();

            if (result.statusCode !== 200) {
                throw new Error('Failed to load tasks');
            }

            const tasks = JSON.parse(result.body);

            if (!Array.isArray(tasks)) {
                throw new Error('Expected an array of tasks');
            }

            currentTasks = tasks;

            tasks.forEach(task => {
                const taskElement = document.createElement('div');
                taskElement.classList.add('task');
                taskElement.innerHTML = `
                    <div>
                        <strong>${task.taskName}</strong>
                        <p>${task.taskDescription}</p>
                    </div>
                    <div class="task-buttons">
                        <button class="updateTaskButton" data-id="${task.taskID}">Update</button>
                        <button class="deleteTaskButton" data-id="${task.taskID}">Delete</button>
                    </div>
                `;
                tasksContainer.appendChild(taskElement);
            });

            addEventListenersToButtons();
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    function getNewTaskId() {
        const existingIds = currentTasks.map(task => parseInt(task.taskID));
        existingIds.sort((a, b) => a - b);
        let newId = 1;
        for (let id of existingIds) {
            if (newId < id) break;
            newId++;
        }
        return newId.toString();
    }

    function addEventListenersToButtons() {
        document.querySelectorAll('.deleteTaskButton').forEach(button => {
            button.addEventListener('click', async (e) => {
                const taskId = e.target.getAttribute('data-id');
                toggleButtons(true);
                try {
                    const response = await fetch(`${endpoint}/tasks/${taskId}`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ pathParameters: { taskID: taskId } })
                    });
                    const result = await response.json();
                    showMessage(result.body.replaceAll('"', ''));
                    loadTasks();
                } catch (error) {
                    console.error('Error deleting task:', error);
                } finally {
                    toggleButtons(false);
                }
            });
        });

        document.querySelectorAll('.updateTaskButton').forEach(button => {
            button.addEventListener('click', async (e) => {
                const taskId = e.target.getAttribute('data-id');
                const newTaskName = prompt('Enter new task name:');
                const newTaskDescription = prompt('Enter new task description:');
                if (newTaskName && newTaskDescription) {
                    toggleButtons(true);
                    try {
                        const response = await fetch(`${endpoint}/tasks/${taskId}`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                pathParameters: { taskID: taskId },
                                body: JSON.stringify({
                                    taskName: newTaskName,
                                    taskDescription: newTaskDescription
                                })
                            })
                        });
                        const result = await response.json();
                        showMessage(result.body.replaceAll('"', ''));
                        loadTasks();
                    } catch (error) {
                        console.error('Error updating task:', error);
                    } finally {
                        toggleButtons(false);
                    }
                }
            });
        });
    }

    function showMessage(message) {
        messageContainer.innerText = message;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 3000);
    }

    function toggleButtons(disabled) {
        document.querySelectorAll('button').forEach(button => {
            button.disabled = disabled;
        });
    }

    loadTasks();
});
