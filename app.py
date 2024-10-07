from flask import Flask, render_template, request, redirect, url_for, jsonify
from gevent import pywsgi
from datetime import datetime as dt
import USERS_DATA as ud
import END as ed
import os

app = Flask(
    __name__,
    static_url_path="/assets",
    static_folder="templates/assets",
    # template_folder='/templates/'
)
app.config["TEMPLATES_AUTO_RELOAD"] = True


"""database."""

file_path = "instance/feedback.csv"
user_file_path = "instance/users.csv"
exam_file_path = "form_download/"

print(f">>> Check if {file_path} is exist ...")
if os.path.exists(file_path):
    print(f"file =>{file_path} already exist")
    print("done.")
else:
    print(f"file =>{file_path} doesn't exist")
    print("Initializing {file_path} ...")
    ud.Init_File(file_path)
    print("done.")

print(f">>> Check if {user_file_path} is exist ...")
if os.path.exists(user_file_path):
    print(f"file =>{user_file_path} already exist")
    print("done.")
else:
    print(f"file =>{user_file_path} doesn't exist")
    print("Initializing {user_file_path} ...")
    ud.Init_File(user_file_path)
    print("done.")

print(f">>> Check if {user_file_path} is exist ...")
if os.path.exists(user_file_path):
    print(f"file =>{user_file_path} already exist")
    print("done.")
else:
    print(f"file =>{user_file_path} doesn't exist")
    print("Initializing {user_file_path} ...")
    ud.Init_File(user_file_path)
    print("done.")

print(f">>> Check if {exam_file_path} is exist ...")
if ed.ensure_directory_exists(exam_file_path) == 0:
    print(f"file =>{exam_file_path} already exist")
    print("done.")
else:
    print(f"file =>{exam_file_path} doesn't exist")
    print("Initializing {exam_file_path} ...")
    print("done.")


"""docstring for router."""


@app.route("/pages/404")
@app.route("/pages/404.html")
def error():
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
    if ud.Identity(user_file_path, uid, pin).back() == 2:
        return render_template("teacher_panel.html")
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/teacher_panel/<uid>/<pin>/<go>")
def teacher_panel_go(uid, pin, go):
    if ud.Identity(user_file_path, uid, pin).back() == 2:
        return render_template(go)
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/student_panel/<uid>/<pin>/")
def student_panel(uid, pin):
    if ud.Identity(user_file_path, uid, pin).back() == 3:
        return render_template("student_panel.html")
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/student_panel/<uid>/<pin>/<go>")
def student_panel_go(uid, pin, go):
    if ud.Identity(user_file_path, uid, pin).back() == 3:
        return render_template(go)
    else:
        return "<h>Cheers! 🥂<h>"


"""form and exam"""


@app.route("/student_panel/<uid>/<pin>/form_submit_e/<id>")
def exam_form_e(uid, pin, id):
    if ud.Identity(user_file_path, uid, pin).back() == 3:
        return render_template(".html")
    else:
        return "<h>Cheers! 🥂<h>"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Save the file to form_download
        save_path = "form_download/" + file.filename
        print(save_path)
        file.save(save_path)
        return jsonify({"message": "File uploaded successfully"}), 200


"""docstring for databack."""


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    ud.Add_Users(name, email, message, file_path).add()

    print(f"Name: {name}, Email: {email}, Message: {message}")

    return render_template("contact.html", success=True)


@app.route("/login", methods=["POST"])
def login():
    uid = request.form.get("uid")
    pin = request.form.get("pin")

    print(f"uid: {uid}, pin: {pin}")
    backdt = ud.Identity(user_file_path, uid, pin).back()
    """ student 3, teacher 2, admin 1 """
    if backdt == 3:
        student_login(uid, pin)
        return redirect(url_for("student_panel", uid=uid, pin=pin), code=302)
    elif backdt == 2:
        teacher_login(uid, pin)
        # redirect to /teacher_panel/<uid>/<pin>
        return redirect(url_for("teacher_panel", uid=uid, pin=pin), code=302)
    elif backdt == 1:
        admin_login(uid, pin)
        return "<h>Admin successfully logged in, but why is there nothing here? 😔<h>"
    else:
        return "<h>User isn't exist, please contact to the admin. Send Email to ohrol@qq.com<h>"


@app.route("/submit_teacherpanel_checkin", methods=["GET"])
def submit_teacherpanel_checkin():
    cclass = request.args.get("cclass")
    print(cclass)
    return ed.show_csv(cclass)


# return "<h>Succesfully logged in.<h>"

"""docstring for ends."""


def student_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin(user_file_path, uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Student {uid} successfull logged in at {check_date}")


def teacher_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin(user_file_path, uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Teacher {uid} successfull logged in at {check_date}")


def admin_login(uid, pin):
    check_date = dt.today()
    ud.Users_Checkin(user_file_path, uid, check_date.strftime("%Y%m%d")).checkin()
    print(f">>> Admin {uid} successfull logged in at {check_date}")


if __name__ == "__main__":
    Site = "localhost"
    Port = 88
    # debug setup
    """app.run(debug=True, port=88, host="localhost")"""
    # wsgi setup
    server = pywsgi.WSGIServer((Site, Port), app)
    print(f">>> Service is running on http://{Site}:{Port}")
    server.serve_forever()
