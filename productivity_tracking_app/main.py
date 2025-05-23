from flask import Flask, render_template, request, redirect, url_for
from chatbot import * 
from tasks import *

app = Flask(__name__)

responses = []

bot = Chatbot()
todo = ToDoList()

@app.route('/', methods=["GET", "POST"])
def home():
    
    # If the user sends asks a question
    if request.method == "POST":

        # Get their question
        chat_data = bot.get_chat_data()

        # Add response to responses
        responses.append(chat_data)
        
        return redirect(url_for('home'))

    bot.write_json("chat.json", responses)

    todo.tasks = bot.read_json("tasks.json")
    view_archive = request.args.get("archived") == "true"

    # New Task
    if request.method == "POST":
        task_name = request.form.get("task")
        desc = request.form.get("description")

        if task_name and desc: 
            new_task = Task(name=task_name, description=desc, completed=False)

            # Adds task to tasks 
            todo.tasks.append(new_task.get_task_data())

            # Saves tasks to json
            bot.write_json("tasks.json", todo.tasks)

        # Redirecting
        return redirect(url_for("home"))
    
    return render_template("index.html", responses=responses, tasks=todo.tasks, view_archive=view_archive)

@app.route("/", methods=["GET", "POST"])
def home():
    
    # Rendering template
    return render_template("index.html", )

# When checkbox is toggled
@app.route("/toggle/<int:index>", methods=["POST"])
def toggle(index):
    tasks = load_tasks()

    if 0 <= index < len(tasks):
        # Gets the status of task - completed or not completed
        current_status = tasks[index].get("completed", False)
        
        # Switches the status of the task
        tasks[index]["completed"] = not current_status

        # Save the updated tasks list back to the json
        save_tasks(tasks)
    
    return redirect(url_for("home"))

@app.route("/clear", methods=["POST"])
def clear():
    tasks = []
    save_tasks(tasks)

    return redirect(url_for("home"))

@app.route("/archived", methods=["POST"])
def archive():
    return redirect(url_for("home", archived="true"))

if __name__ == "__main__":
    app.run(debug=True)