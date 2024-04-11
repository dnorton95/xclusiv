from flask_app import app
from flask_app.models.pie import Pie
from flask_app.models.user import User
from flask_app.models.rating import Rating
from flask import flash, render_template, redirect, request, session

@app.route("/dashboard")
def pies():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    user_id = session["user_id"]
    pies = Pie.find_all_pies_with_users()
    user = User.find_user_by_id(session["user_id"])
    user_pies = Pie.find_pies_by_user_id(user_id)

    return render_template("dashboard.html", pies=pies, user=user, user_pies = user_pies)

@app.get("/pies")
def get_all_pies():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    
    pies = Pie.find_all_pies_with_users_and_ratings()
    user = User.find_user_by_id(session["user_id"])

    for pie in pies:
        pie_ratings = Rating.all_ratings(pie.id)
        pie.total_points = sum(rating.points for rating in pie_ratings)

    return render_template("all_pies.html", pies=pies, user=user)


@app.post("/pies/create")
def create_pie():
    # Check Session for User
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    user_id = session["user_id"]
    # Check Session for User

    # Run pie class validator
    if not Pie.form_is_valid(request.form):
        return redirect("/dashboard")
    # Run pie class validator

    if "ratings" in request.form:
        session["ratings"] = request.form["ratings"]

    # Check if the pie name is unique
    if Pie.count_by_recipe(request.form["recipe"]) >= 1:
        flash("Pie already exists!")
        return redirect("/dashboard")
    # Check if the pie name is unique


    if "ratings" in session:
        session.pop("ratings")

    Pie.create(request.form)
    flash("Pie succesfully posted")
    return redirect("/dashboard")

@app.get("/pies/<int:pie_id>")
def pie_details(pie_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    pie_ratings = Rating.all_ratings(pie_id)
    pie = Pie.find_pie_by_id_with_user(pie_id)
    user = User.find_user_by_id(session["user_id"])
    user_id = session.get('user_id')
    has_submitted_rating = Rating.has_submitted_rating(pie_id, user_id)

    user_rating_id = None  # Initialize user_rating_id

    if has_submitted_rating:
        user_rating_id = Rating.get_user_rating_id(pie_id, user_id)  # Retrieve user's rating ID

    if pie_ratings:
        average_rating = sum(rating.points for rating in pie_ratings) / len(pie_ratings)
    else:
        average_rating = None

    return render_template('pie_details.html', pie=pie, pie_ratings=pie_ratings, user=user, average_rating=average_rating, has_submitted_rating=has_submitted_rating, user_rating_id=user_rating_id)

@app.get("/pies/<int:pie_id>/edit")
def edit_pie(pie_id):

    # Check if user is in session
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    # Check if user is in session
    
    # Pass in the pie and user variables
    pie = Pie.find_pie_by_id(pie_id)
    user = User.find_user_by_id(session["user_id"])
    # Pass in the pie and user variables
    
    return render_template("edit_pie.html", pie=pie, user=user)


@app.post("/pies/update")
def update_pie():
    # Check if user is in session
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    # Check if user is in session
    
    # Check for pie_id
    if "pie_id" not in request.form:
        flash("Pie ID is missing.", "error")
        return redirect("/")
    # Check for pie_id

    pie_id = request.form["pie_id"]
    pie = Pie.find_pie_by_id(pie_id)

    # Check if the pie name is being changed
    if pie.recipe != request.form["recipe"]:
        if Pie.count_by_recipe(request.form["recipe"]) >= 1:
            flash("A pie with this name already exists.", "edit_pie_error")
            return redirect(f"/pies/{pie_id}/edit")

    # Validate the existence of pie_id and other necessary form fields
    if not Pie.form_is_valid(request.form):
        flash("Invalid pie data.", "error")
        return redirect(f"/pies/{pie_id}/edit")
    
    # Update the pie using Pie.update() method
    Pie.update(pie_id, request.form)

    flash("Pie successfully updated")
    return redirect(f"/pies/{pie_id}")

@app.post("/pies/<int:pie_id>/delete")
def delete_pie(pie_id):
    if "user_id" not in session:
        flash("Please log in.")
        return redirect("/")

    user_id = session["user_id"]
    pie = Pie.find_pie_by_id(pie_id)

    # Check if the logged-in user owns the pie
    if pie.user_id != user_id:
        flash("You do not have permission to delete this pie.", "delete_pie_error")
        return redirect("/")

    Pie.delete_by_id(pie_id)
    flash("Pie successfully deleted")
    return redirect("/dashboard")
