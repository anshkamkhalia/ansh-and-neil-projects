from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from google import genai
import datetime as dt
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

from datetime import datetime

# Get today's date
today = datetime.today()

# Format as YYYY-MM-DD
today_str = today.strftime("%Y-%m-%d")

print(today_str)  # e.g. "2025-08-20"

data = [
        "Write down 3 things you have really appreciated from the day today.",
        "Walk for 10 minutes today, without looking at your phone, focused on your surroundings.",
        "Without any judgement or criticism, count how many times your mind gets distracted today.",
        "Every time your phone vibrates or pings today, pause and follow one breath before looking at it.",
        "Brush your teeth with your non-dominant hand today to help encourage attention.",
        "De-clutter part of your house or office today, helping the mind to feel calmer and clearer.",
        "Drink a mindful cup of tea or coffee today, free from other distractions, focused on taste and smell.",
        "Move email and social media apps to the second page of your phone today.",
        "Notice the sensation as you change posture today from standing to sitting or sitting to standing.",
        "Without forcing it, ask someone how they are today and listen to the reply free from opinion.",
        "Commit to no screen time for 2 hours before bed today, other than playing the sleep exercise.",
        "Pause for 60 seconds to follow the breath each time you enter and exit the car/bus/train today.",
        "Sit down and listen to a favorite song or piece of music today, whilst doing nothing else at all.",
        "Take 5 x 2 minute breaks today and simply follow the breath, as you do in your meditation.",
        "Rather than text someone today, call them instead and have a proper conversation.",
        "Check the kids sleeping before going to bed today and follow three of their deep breaths.",
        "Reset your posture each time you sit down today, gently straightening the back.",
        "Give heartfelt thanks to someone today who has recently helped you in some way.",
        "Turn off all notifications on your phone today.",
        "Eat one meal alone today, without any distractions at all, focusing just on the tastes and smells.",
        "Take one full breath (both in and out) before pressing send any email or social post today.",
        "Commute without music today, just for one day and see how much more you notice.",
        "Buy someone a coffee/tea/cake today for no reason, and without expectation of thanks.",
        "Get some exercise today, without your phone, and focus on the physical sensations.",
        "Take 3 x 30 minute breaks from the phone today, set a timer if you need to.",
        "Take one square of chocolate today and allow it to melt in the mouth, enjoying without chewing.",
        "Write a handwritten card/letter to a good friend you've not seen for a long time.",
        "Do something playful, whatever makes you smile or laugh, at least one time today.",
        "When you get to work, or arrive home, today, pause and follow 10 breaths before entering.",
        "Carry some loose change today and share it with people on the street who need it more."
    ]

# ------------------------------------------- HOME ------------------------------------------- 

@app.route("/")
def home():
    return render_template("index.html")

# ------------------------------------------- LOGIN -------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def authentication_page():
    global user_data # Setting global for use all around the program
    global user_logged_in # For global use
    user_data = {} # To keep track of the current user data
    invalid_cred = False

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        action = request.form.get("action") 

        # Handle signup
        if action == "signup":
            # If the user exists 
            new_user_data = {
                "email": email,
                "password": password,
            }
            # Open json file and read contents
            with open('src/data.json','r') as file:
                try:
                    data = json.load(file)
                except:
                    data = [] # Setting as empty list if json file is empty
            
            data.append(new_user_data) # Add new user data to past data

            # Add updated data to the json file
            with open('data.json','w') as file:
                json.dump(data, file, indent=4)

            user_data = new_user_data # Easier naming conventions

            return redirect(url_for('dashboard')) 
        
        # Handle login
        elif action == "login":
            user_logged_in = False # To keep track

            # Open json file and read contents
            with open('data.json','r') as file:
                try:
                    data = json.load(file)
                except:
                    data = []

            # Get the user data
            try:
                for entry in data:
                    if entry["email"] == email and entry["password"] == password:
                        user_data = entry
                        user_logged_in = True
                        invalid_cred = False

                if not user_logged_in:
                    invalid_cred = True
            except:
                user_data = None

            if user_logged_in:
                return redirect(url_for("dashboard"))
            else: pass

    return render_template("auth.html", error="Invalid credentials" if invalid_cred else None)

@app.route("/check-auth")
def get_variable():
    return jsonify(value=user_logged_in)

# ------------------------------------------- DASHBOARD ROUTING -------------------------------------------

@app.route("/dashboard/")
@app.route("/dashboard/<tab>", methods=["GET", "POST"])
def dashboard(tab=None):

    if not user_data:
        return redirect(url_for('authentication_page'))
    
    valid_tabs = {
        None: 'main',
        'journal': 'journal',
        'resources': 'resources',
        'ai': 'ai',
        'guided_breathing': 'guided_breathing',
        'mindfulness_challenge' : 'mindfulness_challenge',
        'crisis_support': ' crisis_support'
    }

    if tab not in valid_tabs:
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', tab=valid_tabs[tab])

# ------------------------------------------- JOURNAL ENTRY -------------------------------------------

@app.route("/dashboard/journal", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        entry = request.form.get("entry") 
        entry_dict = {
            "email": user_data["email"],
            "entry": entry,
            "date": today_str
        }

        # Load existing entries
        try:
            with open('entries.json', 'r') as f:
                entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            entries = []

        # Add new entry
        entries.append(entry_dict)

        # Save back to file
        with open('entries.json', 'w') as f:
            json.dump(entries, f, indent=4)

        flash("Entry saved!", "success")
        return redirect(url_for('dashboard', tab='journal'))

    # If searching by date
    search_date = request.args.get("date")
    searched_entries = []
    try:
        with open('entries.json', 'r') as f:
            entries = json.load(f)
            if search_date:
                searched_entries = [
                    e for e in entries 
                    if e["email"] == user_data["email"] and e["date"] == search_date
                ]
            else:
                # ✅ Show ALL entries for current user if no date is searched
                searched_entries = [
                    e for e in entries if e["email"] == user_data["email"]
                ]
    except (FileNotFoundError, json.JSONDecodeError):
        searched_entries = []

    return render_template(
        'dashboard.html',
        tab="journal",
        searched_entries=searched_entries
    )

# ------------------------------------------- RESOURCES -------------------------------------------
@app.route("/dashboard/resources")
def resources():
    return render_template('dashboard.html', tab="resources")

# ------------------------------------------- AI -------------------------------------------
@app.route('/dashboard/ai', methods=["POST", "GET"])
def ai():
    from google import genai
    import os
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return jsonify({"reply": "API key not found. Please set GEMINI_API_KEY."})

    client = genai.Client(api_key=api_key)

    if not user_data:
        return jsonify({"reply": "User not logged in."})
    global username
    username = user_data['email'].split("@")[0]

    if request.method == "POST":
        user_message = request.json.get("message")
        print(f"[DEBUG] User message: {user_message}")

        gemini_prompt = f"""
        You are a compassionate and professional therapist.
        Provide emotional support, guidance, and encouragement to {username}.
        User says: "{user_message}"

        Instructions:
        1. Be empathetic, patient, and understanding.
        2. Keep responses appropriate, respectful, and safe.
        3. Focus on listening and offering gentle guidance.
        """

        try:
            # 1️⃣ Create chat
            chat = client.chats.create(model="gemini-2.0-flash")

            # 2️⃣ Send the prompt
            response = chat.send_message(gemini_prompt)

            reply_text = response.text if response else "Sorry, I couldn't get a response."
            print(f"[DEBUG] AI reply: {reply_text}")

            return jsonify({"reply": reply_text})

        except Exception as e:
            print(f"[ERROR] Gemini API failed: {e}")
            return jsonify({"reply": "Sorry, the AI is currently unavailable."})

    # GET request just renders the page
    return render_template("dashboard.html", tab="ai")

from flask import session

@app.route("/mindfulness_challenge", methods=["GET", "POST"])
def mindfulness_challenge():
    if "accepted_challenge" not in session:
        session["accepted_challenge"] = False
        session["challenge"] = None
        session["success_msg"] = None

    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "get_challenge":
            session["challenge"] = random.choice(data)
            session["accepted_challenge"] = True
            session["success_msg"] = None
        elif form_type == "finish_challenge":
            username = user_data['email'].split("@")[0]  # get first part of email
            session["success_msg"] = f"Great job, {username}!"

    return render_template(
        "dashboard.html",
        tab='mindfulness_challenge',
        accepted_challenge=session.get("accepted_challenge"),
        challenge=session.get("challenge"),
        success_msg=session.get("success_msg"))
    

@app.route("/dashboard/crisis_support")
def crisis_support():
    return render_template("dashboard.html", tab='crisis_support')

# ------------------------------------------- RUN -------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
