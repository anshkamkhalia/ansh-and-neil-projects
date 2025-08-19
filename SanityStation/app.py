from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# ------------------------------------------- HOME -------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

# ------------------------------------------- LOGIN -------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def authentication_page():
    global user_data # Setting global for use all around the program
    global user_logged_in # For global use
    user_data = None # To keep track of the current user data
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
            with open('data.json','r') as file:
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
@app.route("/dashboard/<tab>")
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
        'crisis_support': 'crisis_support'
    }

    if tab not in valid_tabs:
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', tab=valid_tabs[tab])

# ------------------------------------------- JOURNAL ENTRY -------------------------------------------

@app.route("/dashboard/journal", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        entry = request.form.get("entry") 
        entry_dict = {user_data["email"]: entry}

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

        return redirect(url_for('dashboard', tab='journal'))

    return render_template('dashboard.html', tab="journal")


# ------------------------------------------- RUN -------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
