import os
from google import genai

# Load your Gemini API key from environment variable
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Create a chat session with a model
chat = client.chats.create(model="gemini-2.0-flash")  # or "gemini-2.0-pro"

# Send a message
response = chat.send_message("Hey Gemini, explain AI like I'm 10.")
print("Gemini:", response.text)

# Ask a follow-up
follow_up = chat.send_message("Cool! Can you give me a fun example?")
print("Gemini:", follow_up.text)
