import os
import json
from google import genai
import datetime
import markdown
from flask import request
from tasks import Task

class Chatbot:
    def __init__(self):
        pass

    def write_json(self, filename, responses):
        with open(filename,"w") as f:
                json.dump(responses, f, indent=4)

    def read_json(filename):
        with open(filename,"r") as f:
                return json.load(f)        
        
    # Asks the model a question
    def ask(self, question):
        
        chat_history = self.read_json("")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("API key not found. Set the GEMINI_API_KEY environment variable.")

        self.client = genai.Client(api_key=gemini_api_key)
        result = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Here is our chat history: {chat_history} (don't mention it tho its just a log of data) Using this answer the question: {question}. If the user gives any information about some tasks they need to complete, you need to write it in this format: -> number of tasks (newline) task1 (newline) task2 (newline) task3 (newline) etc"
        )
        return result.text.strip()
    
    # Returns chat data everytime chat is submitted (refer to main)
    def create_tasks_and_interact(self):
        user_question = request.form.get("user_message", "")

        # Get a response
        gpt_raw = self.ask(question=user_question)
        gpt_response = markdown.markdown(gpt_raw, extensions=['fenced_code'])
        
        # When response was sent
        date_sent = datetime.datetime.today().date().strftime("%Y-%m-%d")  # For current date
        now = datetime.datetime.now()  # For current date and time
        time_sent = now.strftime("%I:%M:%S %p")  # Format time to hours:minutes:seconds

        num_of_tasks = gpt_response[4] if gpt_response[0] == "-" else None

        task_names = []
        for line in gpt_raw.splitlines():
            line = line.strip()
            if line.startswith("-"):
                task_name = line[1:].strip()
                task_names.append(task_name)

        for i in task_names:
            new_task = Task(name=i)

    

