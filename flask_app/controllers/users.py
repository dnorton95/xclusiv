# This will be in your controllers folder.  Remember to 'pipenv install flask pymysql flask_bcrypt' in your main project folder!
from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session

# Replace all "Users/user" with your class name!

@app.route("/")
def index():
    return render_template("index.html")



@app.post("/users/register")
def register():
    if not User.validate_register(request.form):
        return redirect("/")

    potential_user = User.find_user_by_email(request.form["email"])

    if potential_user != None:
        flash("Email already in use, please log in!", "register")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_input_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_input_data)
    session["user_id"] = user_id
    return redirect("/dashboard")


@app.post("/users/login")
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    potential_user = User.find_user_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid credentials", "login")
        return redirect("/")

    user = potential_user

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials", "login")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/dashboard")


@app.route("/users/logout")
def logout():
    session.clear()
    return redirect("/")
