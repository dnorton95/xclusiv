from flask_app import app
from flask_app.models.post import post
from flask_app.models.user import User
from flask_app.models.comment import comment
from flask import flash, render_template, redirect, request, session

@app.route("/dashboard")
def posts():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    user_id = session["user_id"]
    posts = post.find_all_posts_with_users()
    user = User.find_user_by_id(session["user_id"])
    user_posts = post.find_posts_by_user_id(user_id)

    return render_template("dashboard.html", posts=posts, user=user, user_posts = user_posts)

@app.get("/posts")
def get_all_posts():
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    
    
    posts = post.find_all_posts_with_users_and_comments()
    user = User.find_user_by_id(session["user_id"])

    for post in posts:
        post_comments = comment.all_comments(post.id)
        post.total_points = sum(comment.points for comment in post_comments)

    return render_template("all_posts.html", posts=posts, user=user)


@app.post("/posts/create")
def create_post():
    # Check Session for User
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    user_id = session["user_id"]
    # Check Session for User

    # Run post class validator
    if not post.form_is_valid(request.form):
        return redirect("/dashboard")
    # Run post class validator

    if "comments" in request.form:
        session["comments"] = request.form["comments"]

    # Check if the post name is unique
    if post.count_by_recipe(request.form["recipe"]) >= 1:
        flash("post already exists!")
        return redirect("/dashboard")
    # Check if the post name is unique


    if "comments" in session:
        session.pop("comments")

    post.create(request.form)
    flash("post succesfully posted")
    return redirect("/dashboard")

@app.get("/posts/<int:post_id>")
def post_details(post_id):
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    post_comments = comment.all_comments(post_id)
    post = post.find_post_by_id_with_user(post_id)
    user = User.find_user_by_id(session["user_id"])
    user_id = session.get('user_id')
    has_submitted_comment = comment.has_submitted_comment(post_id, user_id)

    user_comment_id = None  # Initialize user_comment_id

    if has_submitted_comment:
        user_comment_id = comment.get_user_comment_id(post_id, user_id)  # Retrieve user's comment ID

    if post_comments:
        average_comment = sum(comment.points for comment in post_comments) / len(post_comments)
    else:
        average_comment = None

    return render_template('post_details.html', post=post, post_comments=post_comments, user=user, average_comment=average_comment, has_submitted_comment=has_submitted_comment, user_comment_id=user_comment_id)

@app.get("/posts/<int:post_id>/edit")
def edit_post(post_id):

    # Check if user is in session
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    # Check if user is in session
    
    # Pass in the post and user variables
    post = post.find_post_by_id(post_id)
    user = User.find_user_by_id(session["user_id"])
    # Pass in the post and user variables
    
    return render_template("edit_post.html", post=post, user=user)


@app.post("/posts/update")
def update_post():
    # Check if user is in session
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    # Check if user is in session
    
    # Check for post_id
    if "post_id" not in request.form:
        flash("post ID is missing.", "error")
        return redirect("/")
    # Check for post_id

    post_id = request.form["post_id"]
    post = post.find_post_by_id(post_id)

    # Check if the post name is being changed
    if post.recipe != request.form["recipe"]:
        if post.count_by_recipe(request.form["recipe"]) >= 1:
            flash("A post with this name already exists.", "edit_post_error")
            return redirect(f"/posts/{post_id}/edit")

    # Validate the existence of post_id and other necessary form fields
    if not post.form_is_valid(request.form):
        flash("Invalid post data.", "error")
        return redirect(f"/posts/{post_id}/edit")
    
    # Update the post using post.update() method
    post.update(post_id, request.form)

    flash("post successfully updated")
    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    if "user_id" not in session:
        flash("Please log in.")
        return redirect("/")

    user_id = session["user_id"]
    post = post.find_post_by_id(post_id)

    # Check if the logged-in user owns the post
    if post.user_id != user_id:
        flash("You do not have permission to delete this post.", "delete_post_error")
        return redirect("/")

    post.delete_by_id(post_id)
    flash("post successfully deleted")
    return redirect("/dashboard")
