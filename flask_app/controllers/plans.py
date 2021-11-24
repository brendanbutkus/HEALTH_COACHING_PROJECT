from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.plan import Plan


@app.route('/plans/new')
def new_plan():
    if "user_id" not in session:
        return redirect("/loguot")
    data =  {
        "id":session["user_id"]
    }
    return render_template("new_plan.html", user=User.get_by_id(data))

@app.route("/plans/<int:id>")
def new(id):
    if "user_id" not in session:
        return redirect("/loguot")
    data = {
        "plan_id":id
    }
    plan = Plan.get_one(data)[0]
    print(plan)
    return render_template("view.html", plan=plan)

@app.route("/plans/create", methods=["POST"])
def create_user():
    if "user_id" not in session:
        return redirect ("/logout")
    if not Plan.validate_plan(request.form):
        return redirect ("/plans/new")

    data = {
        "name" : request.form["name"],
        "fitness" : request.form["fitness"],
        "yoga" : request.form["yoga"],
        "meditation" : request.form["meditation"],
        "cold_shower" : request.form["cold_shower"],
        "check_app": request.form["check_app"],
        "frequency": request.form["frequency"],
        "accountable": request.form["accountable"],
        "help": request.form["help"],
        "reminder": request.form["reminder"],
        "user_id": session["user_id"]

    }
    
    Plan.save(data)
    return redirect('/dashboard')
    # return redirect("/plans/create")

@app.route("/plans/edit/<int:id>")
def edit_car(id):
    if "user_id" not in session:
        return redirect("/loguot")
    data = {
        "plan_id":id,
        "user_id":session["user_id"]
    }
    results = Plan.edit_one(data)
    if len(results) > 0:
        plan = results[0]
        return render_template("edit_plan.html", plan=plan)
    return redirect('/dashboard')

@app.route("/plans/update", methods=["POST"])
def update_plan():
    if "user_id" not in session:
        return redirect ("/logout")
    if not Plan.validate_plan(request.form):
        id = request.form["plan_id"]
        return redirect (f"/plans/edit/{id}")

    data = {
        "name" : request.form["name"],
        "fitness" : request.form["fitness"],
        "yoga" : request.form["yoga"],
        "meditation" : request.form["meditation"],
        "cold_shower" : request.form["cold_shower"],
        "check_app": request.form["check_app"],
        "frequency": request.form["frequency"],
        "accountable": request.form["accountable"],
        "help": request.form["help"],
        "reminder": request.form["reminder"],
        "plan_id": session["plan_id"]
    }
    Plan.update(data)
    return redirect("/dashboard") 

@app.route("/plans/destroy/<int:id>")
def destroy_plan(id):
    if "user_id" not in session:
        return redirect("/loguot")
    data = {
        "id":id,
        "user_id": session['user_id']
    }
    Plan.destroy(data)
    return redirect("/dashboard")


