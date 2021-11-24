from flask_app import app
from flask import render_template,redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.plan import Plan
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash
    }
    user_id = User.insert_user(data)
    session["user_id"] = user_id
    flash("User created!")
    return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    data = {
        "email":request.form["email"],
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session["user_id"] = user_in_db.id
    session["user_name"] = user_in_db.first_name 

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("not logged in")
        return redirect("/logout")
    
    return render_template("dashboard.html", plans=Plan.get_all())

@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return redirect("/")