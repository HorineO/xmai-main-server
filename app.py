from flask import Flask, render_template, request
from markupsafe import escape
from gevent import pywsgi
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    static_url_path="/assets",
    static_folder="templates/assets",
    # template_folder='/templates/'
)
app.config["TEMPLATES_AUTO_RELOAD"] = True

"""database."""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


with app.app_context():
    db.create_all()


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

    new_user = User(username=name, email=email, message=message)
    db.session.add(new_user)
    db.session.commit()

    # 在这里处理表单数据，例如保存到数据库或发送邮件
    print(f"Name: {name}, Email: {email}, Message: {message}")

    return render_template("contact.html", success=True)


if __name__ == "__main__":
    # debug setup
    """app.run(debug=True, port=88, host="localhost")"""
    # wsgi setup
    server = pywsgi.WSGIServer(('localhost',88),app)
    server.serve_forever()
