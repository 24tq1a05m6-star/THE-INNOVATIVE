from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)
app.secret_key = "secret123"   

conn = sqlite3.connect("ideas.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    idea TEXT,
    user TEXT
)
""")

conn.commit()
conn.close()

notes = []

users = {
    "naveenpinniboina3@gmail.com": "NAVEEN7005",
    "tadudarisaiadvaith@gmail.com": "#TSA2006",
    "kumarsanthosh40466@gmail.com": "ammulu12",
    "24tq1a05p5@siddhartha.co.in":"NAVEEN@949",
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form.get("email")
        password = request.form.get("password")

        if student_id in users and users[student_id] == password:
            session["user"] = student_id
            return redirect("/dashboard")
        else:
            return "Invalid credentials ❌"

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("ideas.db")
    c = conn.cursor()

    c.execute("SELECT title, idea, user FROM ideas")
    ideas = c.fetchall()

    conn.close()

    return render_template("dashboard.html", user=session["user"], ideas=ideas)
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/notifications", methods=["GET", "POST"])
def notifications():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        title = request.form.get("title")
        message = request.form["message"]
        image = request.form["image"]

        notes.append({
            "title": title,
            "message": message,
            "image": image
        })

    return render_template("notifications.html", notes=notes)


@app.route("/post", methods=["GET", "POST"])
def post():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        title = request.form["title"]
        idea = request.form["idea"]

        conn = sqlite3.connect("ideas.db")
        c = conn.cursor()

        c.execute("INSERT INTO ideas (title, idea, user) VALUES (?, ?, ?)",
                  (title, idea, session["user"]))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("post.html")

if __name__ == "__main__":
    app.run(debug=True)
