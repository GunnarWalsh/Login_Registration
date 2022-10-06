from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 


@app.route("/")
def login_home():
    return render_template("home.html")

@app.route("/dashboard")
def home():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", this_user = user.User.get_user_by_id(data))

@app.route("/register" , methods=["POST"])
def user_register():
    if not user.User.validate_reg(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    session["user_id"] = user.User.register_user(data)
    return redirect("/dashboard")

@app.route("/login" , methods=["POST"])
def user_login():
    got_user = user.User.validate_login(request.form)
    if not got_user:
        return redirect("/")
    session["user_id"] = got_user.id
    return redirect ("/dashboard")

@app.route("/logout")
def user_logout():
    session.clear()
    return redirect('/')