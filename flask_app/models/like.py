from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

class like:
    DB = "posts_schema"


    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.comment_id = data["comment_id"]
        self.upvote = data["upvote"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = {
            "id": data["user_id"],  # Use 'user_id' instead of 'users.id'
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        }
        self.like_id = data["id"]  # Renamed from 'id' to 'like_id'

    @classmethod
    def all_likes(cls, post_id):
        data = {"post_id": post_id}
        query = """SELECT *
                FROM likes
                JOIN users ON likes.user_id = users.id
                WHERE likes.post_id = %(post_id)s
                ORDER BY likes.created_at DESC; """
        list_of_dicts = connectToMySQL(like.DB).query_db(query, data)
        pprint(list_of_dicts)

        likes = []
        for each_dict in list_of_dicts:
            like = like(each_dict)
            likes.append(like)
        return likes

    @classmethod
    def create(cls, form_data):
        # Convert the 'points' value to an integer
        form_data['points'] = int(form_data['points'])
        
        query = """INSERT INTO likes (user_id, post_id, points) 
                VALUES (%(user_id)s, %(post_id)s, %(points)s);"""
        connectToMySQL("posts_schema").query_db(query, form_data)
        return


    @classmethod
    def delete_like(cls, like_id):
        query = """DELETE FROM likes WHERE id = %(like_id)s"""
        data = {"like_id": like_id}
        connectToMySQL(like.DB).query_db(query, data)
        return
    
    @classmethod
    def has_submitted_like(cls, post_id, user_id):
        query = "SELECT COUNT(*) FROM likes WHERE post_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (post_id, user_id))
        return result[0]['COUNT(*)'] > 0

    @classmethod
    def get_user_like_id(cls, post_id, user_id):
        query = "SELECT id FROM likes WHERE post_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (post_id, user_id))
        if result:
            return result[0]['id']
        return None