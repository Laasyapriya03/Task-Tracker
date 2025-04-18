from flask import Flask, jsonify, request
import os
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

TASK_FILE = "tasks.txt"
BACKUP_FILE = "tasks_backup.txt"

# Load tasks from the file
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r", encoding="utf-8") as file:
        tasks = []
        for line in file:
            if "::" in line:
                text, status = line.strip().rsplit("::", 1)
                tasks.append({"text": text, "done": status == "done"})
            else:
                tasks.append({"text": line.strip(), "done": False})
    return tasks

# Save tasks to the file
def save_tasks(tasks):
    if os.path.exists(TASK_FILE):
        shutil.copy(TASK_FILE, BACKUP_FILE)
    with open(TASK_FILE, "w", encoding="utf-8") as file:
        for task in tasks:
            status = "done" if task["done"] else "not_done"
            file.write(f"{task['text']}::{status}\n")

# Route for the root URL
@app.route('/')
def index():
    return "Welcome to the Task Tracker API!"

# Route to handle GET (fetch tasks) and POST (add task)
@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = load_tasks()
        return jsonify(tasks)

    if request.method == 'POST':
        new_task = request.json.get("text")
        if new_task:
            tasks = load_tasks()
            tasks.append({"text": new_task, "done": False})
            save_tasks(tasks)
            return jsonify({"message": "Task added!"}), 201
        return jsonify({"message": "Task text is required!"}), 400

# Route to handle PUT (mark task as done) and DELETE (delete task)
@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def update_task(task_id):
    tasks = load_tasks()
    if task_id < 1 or task_id > len(tasks):
        return jsonify({"message": "Invalid task ID!"}), 400

    if request.method == 'PUT':
        tasks[task_id - 1]['done'] = not tasks[task_id - 1]['done']
        save_tasks(tasks)
        return jsonify({"message": "Task updated!"})

    if request.method == 'DELETE':
        deleted_task = tasks.pop(task_id - 1)
        save_tasks(tasks)
        return jsonify({"message": f"Task '{deleted_task['text']}' deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
