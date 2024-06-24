from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.comment import comment



class post:
    DB = "posts_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.emotion = data["emotion"]
        self.location = data["location"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"] 
        self.user = User.find_user_by_id(self.user_id)  

    @staticmethod
    def form_is_valid(post_input_data):
        is_valid = True
        # Text Validator
        if len(post_input_data["recipe"]) == 0:
            flash("Please enter recipe.")
            is_valid = False
        elif len(post_input_data["recipe"]) < 3:
            flash("Recipe must be at least three characters.")
            is_valid = False

        if len(post_input_data["filling"]) == 0:
            flash("Please enter filling.")
            is_valid = False
        elif len(post_input_data["filling"]) < 3:
            flash("Filling field must be at least three characters.")
            is_valid = False

        if len(post_input_data["crust"]) == 0:
            flash("Please enter crust.")
            is_valid = False
        elif len(post_input_data["crust"]) < 3:
            flash("Crust field must be at least three characters.")
            is_valid = False


        return is_valid

    @classmethod
    def find_all_posts(cls):
        query = """SELECT * FROM posts JOIN users ON posts.user_id = users.id"""
        list_of_dicts = connectToMySQL(post.DB).query_db(query)

        posts = []
        for each_dict in list_of_dicts:
            post = post(each_dict)
            posts.append(post)
        return posts
    
    @classmethod
    def get_all_posts(cls):
        query = """
            SELECT posts.*, users.id as user_id, users.first_name, users.last_name
            FROM posts
            JOIN users ON posts.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        
        all_posts = []
        for result in results:
            post_data = {
                "id": result["id"],
                "recipe": result["recipe"],
                "filling": result["filling"],
                "crust": result["crust"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
                "user_id": {
                }
            }
            post = post(post_data)
            all_posts.append(post)
        
        return all_posts

    
    @classmethod
    def find_all_posts_with_users(cls):
        query = """SELECT * FROM posts JOIN users ON posts.user_id = users.id"""

        list_of_dicts = connectToMySQL(post.DB).query_db(query)

        posts = []
        for each_dict in list_of_dicts:
            post = post(each_dict)
            user_input_data = {
                "id": each_dict["id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["created_at"],
                "updated_at": each_dict["updated_at"],
            }
            user = User(user_input_data)
            post.user = user
            posts.append(post)
        return posts
    
    @classmethod
    def find_post_by_id(cls, posts_id):
        """this method finds a post by the ID"""
        query = """SELECT * FROM posts WHERE id = %(posts_id)s"""
        data = {"posts_id": posts_id}
        list_of_dicts = connectToMySQL(post.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        post = post(list_of_dicts[0])
        return post
    
    @classmethod
    def find_post_by_id_with_user(cls, posts_id):
        """This method find a post by the id and user by the record id"""
        query = """
            SELECT posts.*, users.*
            FROM posts
            JOIN users ON posts.user_id = users.id 
            WHERE posts.id = %(posts_id)s
        """

        data = {"posts_id": posts_id}
        list_of_dicts = connectToMySQL(post.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        post = post(list_of_dicts[0])
        user_input_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        post.user = User(user_input_data)
        return post


    
    @classmethod
    def new_post(cls, post_input_data):
        try:
            # Insert post data into the posts table
            query_post = """
            INSERT INTO posts
            (recipe, filling, crust, user_id)
            VALUES
            (%(recipe)s, %(filling)s, %(crust)s, %(user_id)s)
            """
            posts_id = connectToMySQL(cls.DB).query_db(query_post, post_input_data)

            return posts_id
        except Exception as e:
            # Handle the error
            print(f"An error occurred: {str(e)}")
            return None
        
    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO posts
        (recipe, filling, crust, user_id)
        VALUES
        (%(recipe)s, %(filling)s, %(crust)s, 
        %(user_id)s)"""
        post_id = connectToMySQL(post.DB).query_db(query, form_data)
        return post_id
    
    @classmethod
    def update(cls, posts_id, post_input_data):
        query = "UPDATE posts SET recipe = %(recipe)s, filling = %(filling)s, crust = %(crust)s WHERE id = %(posts_id)s;"
        data = {
            "posts_id": posts_id,
            "recipe": post_input_data["recipe"],
            "filling": post_input_data["filling"],
            "crust": post_input_data["crust"],
        }
        connectToMySQL(post.DB).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls, post_id):
        query = "DELETE FROM posts WHERE id = %(post_id)s"
        data = {"post_id": post_id}
        connectToMySQL(post.DB).query_db(query, data)
        return
    
    @classmethod
    def count_by_recipe(cls, recipe):
        query = """SELECT COUNT(recipe) AS "count"
        FROM posts WHERE recipe = %(recipe)s"""
        data = {"recipe": recipe}
        list_of_dicts = connectToMySQL(post.DB).query_db(query, data)
        print(list_of_dicts)
        return list_of_dicts[0]["count"]
    
    @classmethod
    def find_posts_by_user_id(cls, user_id):
        """Find posts associated with a specific user"""
        query = """
            SELECT posts.*, users.*
            FROM posts
            JOIN users ON posts.user_id = users.id 
            WHERE users.id = %(user_id)s
        """

        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(post.DB).query_db(query, data)

        posts = []
        for post_data in list_of_dicts:
            post = post(post_data)

            user_input_data = {
                "id": post_data["users.id"],
                "first_name": post_data["first_name"],
                "last_name": post_data["last_name"],
                "email": post_data["email"],
                "password": post_data["password"],
                "created_at": post_data["users.created_at"],
                "updated_at": post_data["users.updated_at"],
            }
            post.user = User(user_input_data)
            posts.append(post)

        return posts
    
    @classmethod
    def find_all_posts_with_users_and_comments(cls):
        query = """
            SELECT 
                posts.*, 
                users.id AS user_id, 
                users.first_name, 
                users.last_name,
                comments.id AS comment_id, 
                comments.points, 
                comments.post_id,
                users.id AS user_id  -- Alias the users.id column
            FROM 
                posts
            JOIN 
                users ON posts.user_id = users.id
            LEFT JOIN 
                comments ON posts.id = comments.post_id
            ORDER BY 
                posts.id, 
                comments.created_at DESC

        """
        results = connectToMySQL(cls.DB).query_db(query)

        posts = []
        current_post = None
        for result in results:
            if not current_post or current_post.id != result["id"]:
                current_post = cls(result)
                current_post.comments = []  # Initialize comments list for the current post
                posts.append(current_post)

            if result["comment_id"]:  # If there is a comment associated with the post
                current_post.comments.append(comment(result))  # Add the comment to the current post's comments list

        return posts

