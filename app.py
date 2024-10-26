from flask import Flask, render_template, request, redirect, url_for, jsonify
from gevent import pywsgi
from datetime import datetime as dt
import USERS_DATA as ud
import END as ed
import os
import exam as ex

app = Flask(
    __name__,
    static_url_path="/assets",
    static_folder="templates/assets",
    # template_folder='/templates/'
)
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Check and initialize file
def check_and_init_file(file_path, init_func):
    if os.path.exists(file_path):
        print(f"file => {file_path} already exist")
    else:
        print(f"file => {file_path} doesn't exist")
        print(f"Initializing {file_path} ...")
        init_func(file_path)
        print("done.")


file_paths = [
    ("instance/feedback.csv", ud.Init_File),
    ("instance/users.csv", ud.Init_File),
    ("form_download/", ed.ensure_directory_exists),
    ("form_output/", ed.ensure_directory_exists),
]

for file_path, init_func in file_paths:
    check_and_init_file(file_path, init_func)


# Route definitions
@app.route("/pages/404")
@app.route("/pages/404.html")
def error_404():
    return render_template("404.html")


@app.route("/pages/405")
@app.route("/pages/405.html")
def error_405():
    return render_template("405.html")


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/pages/about")
@app.route("/pages/about.html")
def about():
    return render_template("about.html")


@app.route("/pages/contact")
@app.route("/pages/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/pages/sign-in")
@app.route("/pages/sign-in.html")
def sign_in():
    return render_template("sign-in.html")


@app.route("/teacher_panel/<uid>/<pin>/")
def teacher_panel(uid, pin):
    if ud.Identity("instance/users.csv", uid, pin).back() == 2:
        return render_template("teacher_panel.html")
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/teacher_panel/<uid>/<pin>/<go>")
def teacher_panel_go(uid, pin, go):
    if ud.Identity("instance/users.csv", uid, pin).back() == 2:
        return render_template(go)
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/student_panel/<uid>/<pin>/")
def student_panel(uid, pin):
    if ud.Identity("instance/users.csv", uid, pin).back() == 3:
        return render_template("student_panel.html")
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/student_panel/<uid>/<pin>/<go>")
def student_panel_go(uid, pin, go):
    if ud.Identity("instance/users.csv", uid, pin).back() == 3:
        return render_template(go)
    else:
        return "<h>Cheers! 🥂<h>"


@app.route(
    "/student_panel/<uid>/<pin>/student_panel_exam.html/upload", methods=["POST"]
)
def upload_file(uid, pin):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        if ud.Identity("instance/users.csv", uid, pin).back() == 3:
            save_path = f"form_download/{uid} {pin} {file.filename}"
            file.save(save_path)
            return jsonify({"message": "File uploaded successfully"}), 200
        else:
            return jsonify({"error": "Unauthorized access"}), 403


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    ud.Add_Users(name, email, message, "instance/feedback.csv").add()

    print(f"Name: {name}, Email: {email}, Message: {message}")

    return render_template("contact.html", success=True)


@app.route("/login", methods=["POST"])
def login():
    uid = request.form.get("uid")
    pin = request.form.get("pin")

    backdt = ud.Identity("instance/users.csv", uid, pin).back()
    if backdt == 3:
        student_login(uid, pin)
        return redirect(url_for("student_panel", uid=uid, pin=pin), code=302)
    elif backdt == 2:
        teacher_login(uid, pin)
        return redirect(url_for("teacher_panel", uid=uid, pin=pin), code=302)
    elif backdt == 1:
        admin_login(uid, pin)
        return "<h>Admin successfully logged in, but why is there nothing here? 😔<h>"
    else:
        return "<h>User isn't exist, please contact to the admin.<h>"


@app.route("/submit_teacherpanel_checkin", methods=["GET"])
def submit_teacherpanel_checkin():
    cclass = request.args.get("cclass")
    print(cclass)
    return ed.show_csv(cclass)


@app.route("/lete")
@app.route("/submit_teacherpanel_form", methods=["GET"])
def submit_teacherpanel_form():
    fclass = request.args.get("fclass")
    return ex.show_student_info(fclass)


def student_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin("instance/users.csv", uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Student {uid} successfully logged in at {check_date}")


def teacher_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin("instance/users.csv", uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Teacher {uid} successfully logged in at {check_date}")


def admin_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin("instance/users.csv", uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Admin {uid} successfully logged in at {check_date}")


if __name__ == "__main__":
    Site = "localhost"
    Port = 88
    server = pywsgi.WSGIServer((Site, Port), app)
    print(f">>> Service is running on http://{Site}:{Port}")
    server.serve_forever()
