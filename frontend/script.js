document.addEventListener("DOMContentLoaded", loadTasks);

const apiUrl = "http://127.0.0.1:5000/tasks";  // Updated API URL for tasks

// Load tasks from the backend
function loadTasks() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById("task-list");
            taskList.innerHTML = "";  // Clear existing tasks
            tasks.forEach((task, index) => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span onclick="toggleTask(${index + 1})">${task.done ? "[✔]" : "[ ]"} ${task.text}</span>
                    <button onclick="deleteTask(${index + 1})">Delete</button>
                `;
                taskList.appendChild(li);
            });
        });
}

// Add a new task
function addTask() {
    const newTaskInput = document.getElementById("new-task");
    const taskText = newTaskInput.value.trim();
    if (taskText) {
        fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: taskText }),
        })
        .then(response => response.json())
        .then(() => {
            newTaskInput.value = "";  // Clear the input field
            loadTasks();  // Reload tasks after adding
        });
    }
}

// Toggle task completion (mark as done or undone)
function toggleTask(taskId) {
    fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
        method: "PUT",
    })
    .then(response => response.json())
    .then(() => loadTasks());  // Reload tasks after updating
}

// Delete a task
function deleteTask(taskId) {
    fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(() => loadTasks());  // Reload tasks after deletion
}
