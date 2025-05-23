import datetime as dt

class Task:
    def __init__(self, name, description, completed):
        self.name = name
        self.date = str(dt.datetime.now().date())
        self.completed = completed

    def get_task_data(self):
        task_data = {
                "name": self.name,
                "date": self.date,
                "completed": self.completed
            }
        return task_data
    
class ToDoList:
    def __init__(self):
        tasks = []
        pass

    # When user adds task, this runs
    def user_add_task(self):
        # Get task data
        task_name = request.form.get("task")

        if task_name and desc: 
            new_task = Task(name=task_name, description=desc, completed=False)

            return new_task
    
    # When user checks checkbox, this runs
    def user_check_checkbox(self, index):
        if 0 <= index < len(self.tasks):
            # Gets the status of task - completed or not completed
            current_status = self.tasks[index].get("completed", False)
            
            # Switches the status of the task
            self.tasks[index]["completed"] = not current_status

            # Save the updated tasks list back to the json


# tasks.append(new_task.get_task_data())
# then save tasks