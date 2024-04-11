from flask_app import app
from flask_app.models.rating import Rating
from flask import flash, render_template, redirect, request, session

@app.post("/ratings/create")
def create_rating():
    print("Before retrieving pie_id from form")
    pie_id = request.form.get("pie_id")  # Use get method to avoid KeyError
    print("Pie ID from form:", pie_id)  # Add this line for debugging

    form_data = dict(request.form)  # Convert ImmutableMultiDict to a mutable dictionary
    
    # Access and modify form data as needed
    form_data['points'] = int(form_data['points'])
    print("Form data:", form_data)
    
    try:
        # Call the create method of the Rating class with the modified form data
        Rating.create(form_data)
    except Exception as e:
        # Print out the exception to debug the issue
        print("Error occurred:", e)
        flash('Error occurred while creating the rating. Please try again later.', 'error')
    
    # Redirect to a relevant page after handling the form submission
    return redirect(f"/pies/{pie_id}")


@app.post("/ratings/<int:rating_id>/delete")
def rating_delete(rating_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    rating_id = request.form["rating_id"]
    pie_id = request.form["pie_id"]

    Rating.delete_rating(rating_id)
    flash('Vote removed')


    return redirect("/pies")
