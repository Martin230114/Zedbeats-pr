from flask import Flask, render_template, request, redirect, session
import json
import os
print("FILE:", __file__)
print("CWD:", os.getcwd())
print("TEMPLATES EXISTS:", os.path.exists("templates"))
print("BASE DIR:", os.path.dirname(os.path.abspath(__file__)))
print("TEMPLATES EXISTS:", os.path.exists("templates"))
print("HOME EXISTS:", os.path.exists("templates/home.html"))
print("TEMPLATES LIST:", os.listdir("templates"))
print("RUNNING FROM:", os.getcwd())
app = Flask(__name__)
app.secret_key = "Martin230114*"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#---------- Admin storage ----------

def load_admin():
    if not os.path.exists("admin.json"):
        return {}
    with open("admin.json", "r") as f:
        return json.load(f)

def save_admin(data):
    with open("admin.json", "w") as f:
        json.dump(data, f)

#---------- Routes ----------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return redirect("/")
    files = os.listdir("static/uploads")
    results = [f for f in files if query. lower() in f.lower()]
    return render_templates("search.html", results = results)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = load_admin()

        username = request.form["username"]
        password = request.form["password"]

        if username == data["username"] and password == data["password"]:
            session["admin"] = True
            return redirect("/admin")

        return "Invalid credentials"
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/")
    return render_template("admin.html")

@app.route("/admin/upload", methods=["GET", "POST"])
def upload():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        file = request.files["file"]
    os.makedirs("static/uploads", exist_ok=True)
    if file:
        file.save(os.path.join("static/uploads", file.filename))
        return redirect("/media")

    return render_template("upload.html")

@app.route("/media")
def media():
    files = os.listdir("static/uploads")
    music = [f for f in files if f.endswith("mp3")]
    videos  = [f for f in files if f.endswith("mp4")]
    return render_template("media.html", music=music, videos=videos)

@app.route("/media/music")
def music():
    files = os.listdir("static/uploads")
    music = [f for f in files if f.endswith(".mp3")]
    return render_template("music.html")

@app.route("/media/videos")
def videos():
    files = os.listdir("static/uploads")
    videos = [f for f in files if f.endswith(".mp4")]
    return render_template("videos.html")

@app.route("/media/videos/<filename>")
def play_video(filename):
    return render_template("playvideo.html", file = filename)


@app.route("/media/music/<filename>")
def play_music(filename):
    return render_template("playmusic.html", file = filename)

@app.route("/reset", methods=["GET", "POST"])
def reset():
    if not session.get("admin"):
        return "unauthorized"
    if request.method == "POST":
        new_pass = request.form["password"]
        data = load_admin()
        data ["password"] = new_password
        save_admin(data)
        return redirect ("/admin")
    return render_template("reset.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=7000, debug=True)
