from flask import Flask, render_template, request, redirect, session
import json
import os
import cloudinary
import cloudinary.uploader
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
cloudinary.config(
    cloud_name="dbajlwg84",
    api_key="332143418544659",
    api_secret="IVMdokuZlEVfTNF4m_AV50Mq53M")

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

# =========================
# ADMIN UPLOAD ROUTE
# =========================
@app.route("/admin/upload", methods=["GET", "POST"])
def upload():
    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":
        print("UPLOAD STARTED")
        print("FORM:", request.form)
        print("FILES:", request.files)
        title = request.form["title"]
        file = request.files["file"]
        print("TITLE:", title)
        print("FILENAME:", file.filename)
        try:
            result = cloudinary.uploader.upload(
            file,
            resource_type="auto"
        )
            print("UPLOAD RESULT:", result)

        except Exception as e:
            print("CLOUDINARY ERROR:", e)
            return "Upload failed"
        # Upload to Cloudinary
            result = cloudinary.uploader.upload(
            file,
            resource_type="auto"
        )

        # Load existing media list
        try:
            with open("media.json", "r") as f:
                media = json.load(f)
        except:
            media = []

        # New media entry
        media_item = {
            "title": title,
            "filename": file.filename,
            "url": result["secure_url"]
        }

        # Add without deleting old uploads
        media.append(media_item)

        # Save updated media list
        with open("media.json", "w") as f:
            json.dump(media, f, indent=4)

        return redirect("/media")

    return render_template("upload.html")


# =========================
# MEDIA DISPLAY ROUTE
# =========================
@app.route("/media")
def media():
    try:
        with open("media.json", "r") as f:
            files = json.load(f)
    except:
        files = []

    # Separate music and videos
    music = [
        file for file in files
        if file["filename"].lower().endswith((".mp3", ".wav", ".ogg"))
    ]

    videos = [
        file for file in files
        if file["filename"].lower().endswith((".mp4", ".mov", ".avi", ".mkv"))
    ]

    return render_template(
        "media.html",
        music=music,
        videos=videos
    )

@app.route("/media/videos")
def videos():
    with open("media.json", "r") as f:
        files = json.load(f)
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
