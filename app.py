from flask import Flask, render_template, request
from gevent import pywsgi
from flask_sqlalchemy import SQLAlchemy
import USERS_DATA as ud
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

print('>>> Check if {file_path} is exist ...')
if os.path.exists(file_path):
    print(f"file =>{file_path} allready exist")
    print("done.")
else:
    print(f"file =>{file_path} doesn`t exist")
    print("Initializing {file_path} ...")
    ud.Init_File(file_path)
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


"""docstring for databack."""


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    ud.Add_Users(name, email, message, file_path).add()

    print(f"Name: {name}, Email: {email}, Message: {message}")

    return render_template("contact.html", success=True)


if __name__ == "__main__":
    # debug setup
    """app.run(debug=True, port=88, host="localhost")"""
    # wsgi setup
    server = pywsgi.WSGIServer(("localhost", 88), app)
    print('>>> Service is running')
    server.serve_forever()