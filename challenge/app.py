from flask import Flask, request, g, render_template, redirect, url_for, flash, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

ORGANIZERS = [
    ("djinane", "djinane"),
    ("nour", "nour"),
    ("ikram", "ikram"),
    ("amar", "amar"),
    ("omar", "omar"),
    ("anis", "anis"),
    ("salsabila", FLAG),
    ("ines", "ines"),
    ("manel", "manel"),
    ("besmala", "besmala"),
    ("imen", "imen"),
]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("BLIND_CHALLENGE.db")
        cursor = g.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizers (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        cursor.executemany("INSERT OR IGNORE INTO organizers (username, password) VALUES (?, ?)", ORGANIZERS)
        g.db.commit()
        cursor.close()
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    db = get_db()
    cursor = db.cursor()

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    try:
        query = f"SELECT * FROM organizers WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        if result:
            session["logged_in"] = True  
            session["username"] = username  
            if result[0] == 'salsabila':
                flash("You found the imposter now what is she hiding ?")
                return redirect(url_for("index"))  
            else:
                return redirect(url_for("home"))  
        else:
            raise ValueError("Incorrect username or password")
    except Exception as e:
        error = "Error: {}".format(str(e))
        return render_template("index.html", error=error), 404

@app.route("/home")
def home():
    if "logged_in" not in session:
        return redirect(url_for("index"))  
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)  
    session.pop("username", None)  
    return redirect(url_for("index"))  

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
