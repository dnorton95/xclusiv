from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

class comment:
    DB = "posts_schema"


    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.post_id = data["post_id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = {
            "id": data["user_id"],  # Use 'user_id' instead of 'users.id'
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        }
        self.comment_id = data["id"]  # Renamed from 'id' to 'comment_id'

    @classmethod
    def all_comments(cls, post_id):
        data = {"post_id": post_id}
        query = """SELECT *
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.post_id = %(post_id)s
                ORDER BY comments.created_at DESC; """
        list_of_dicts = connectToMySQL(comment.DB).query_db(query, data)
        pprint(list_of_dicts)

        comments = []
        for each_dict in list_of_dicts:
            comment = comment(each_dict)
            comments.append(comment)
        return comments

    @classmethod
    def create(cls, form_data):
        # Convert the 'points' value to an integer
        form_data['points'] = int(form_data['points'])
        
        query = """INSERT INTO comments (user_id, post_id, points) 
                VALUES (%(user_id)s, %(post_id)s, %(points)s);"""
        connectToMySQL("posts_schema").query_db(query, form_data)
        return


    @classmethod
    def delete_comment(cls, comment_id):
        query = """DELETE FROM comments WHERE id = %(comment_id)s"""
        data = {"comment_id": comment_id}
        connectToMySQL(comment.DB).query_db(query, data)
        return
    
    @classmethod
    def has_submitted_comment(cls, post_id, user_id):
        query = "SELECT COUNT(*) FROM comments WHERE post_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (post_id, user_id))
        return result[0]['COUNT(*)'] > 0

    @classmethod
    def get_user_comment_id(cls, post_id, user_id):
        query = "SELECT id FROM comments WHERE post_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (post_id, user_id))
        if result:
            return result[0]['id']
        return None