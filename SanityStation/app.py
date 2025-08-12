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
    user_data = None # To keep track of the current user data
    invalid_cred = False

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        action = request.form.get("action") 

        # Handle signup
        if action == "signup":
             
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

            return redirect(url_for('authentication_page')) # Change to dashboard later
        
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
                return redirect(url_for("home")) # Take user to homepage
            else: pass

    return render_template("auth.html", error="Invalid credentials" if invalid_cred else None)


# ------------------------------------------- RUN -------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
