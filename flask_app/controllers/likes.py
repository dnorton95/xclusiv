from flask_app import app
from flask_app.models.like import like
from flask import flash, render_template, redirect, request, session

@app.post("/likes/create")
def create_like():
    print("Before retrieving post_id from form")
    post_id = request.form.get("post_id")  # Use get method to avoid KeyError
    print("post ID from form:", post_id)  # Add this line for debugging

    form_data = dict(request.form)  # Convert ImmutableMultiDict to a mutable dictionary
    
    # Access and modify form data as needed
    form_data['points'] = int(form_data['points'])
    print("Form data:", form_data)
    
    try:
        # Call the create method of the like class with the modified form data
        like.create(form_data)
    except Exception as e:
        # Print out the exception to debug the issue
        print("Error occurred:", e)
        flash('Error occurred while creating the like. Please try again later.', 'error')
    
    # Redirect to a relevant page after handling the form submission
    return redirect(f"/posts/{post_id}")


@app.post("/likes/<int:like_id>/delete")
def like_delete(like_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    like_id = request.form["like_id"]
    post_id = request.form["post_id"]

    like.delete_like(like_id)
    flash('Vote removed')


    return redirect("/posts")