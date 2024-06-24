from flask_app import app
from flask_app.models.comment import comment
from flask import flash, render_template, redirect, request, session

@app.post("/comments/create")
def create_comment():
    print("Before retrieving post_id from form")
    post_id = request.form.get("post_id")  # Use get method to avoid KeyError
    print("post ID from form:", post_id)  # Add this line for debugging

    form_data = dict(request.form)  # Convert ImmutableMultiDict to a mutable dictionary
    
    # Access and modify form data as needed
    form_data['points'] = int(form_data['points'])
    print("Form data:", form_data)
    
    try:
        # Call the create method of the comment class with the modified form data
        comment.create(form_data)
    except Exception as e:
        # Print out the exception to debug the issue
        print("Error occurred:", e)
        flash('Error occurred while creating the comment. Please try again later.', 'error')
    
    # Redirect to a relevant page after handling the form submission
    return redirect(f"/posts/{post_id}")


@app.post("/comments/<int:comment_id>/delete")
def comment_delete(comment_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    comment_id = request.form["comment_id"]
    post_id = request.form["post_id"]

    comment.delete_comment(comment_id)
    flash('Vote removed')


    return redirect("/posts")
