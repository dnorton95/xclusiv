from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from pprint import pprint

class Rating:
    DB = "pies_schema"


    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.pie_id = data["pie_id"]
        self.points = data["points"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = {
            "id": data["user_id"],  # Use 'user_id' instead of 'users.id'
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        }
        self.rating_id = data["id"]  # Renamed from 'id' to 'rating_id'

    @classmethod
    def all_ratings(cls, pie_id):
        data = {"pie_id": pie_id}
        query = """SELECT *
                FROM ratings
                JOIN users ON ratings.user_id = users.id
                WHERE ratings.pie_id = %(pie_id)s
                ORDER BY ratings.created_at DESC; """
        list_of_dicts = connectToMySQL(Rating.DB).query_db(query, data)
        pprint(list_of_dicts)

        ratings = []
        for each_dict in list_of_dicts:
            rating = Rating(each_dict)
            ratings.append(rating)
        return ratings

    @classmethod
    def create(cls, form_data):
        # Convert the 'points' value to an integer
        form_data['points'] = int(form_data['points'])
        
        query = """INSERT INTO ratings (user_id, pie_id, points) 
                VALUES (%(user_id)s, %(pie_id)s, %(points)s);"""
        connectToMySQL("pies_schema").query_db(query, form_data)
        return


    @classmethod
    def delete_rating(cls, rating_id):
        query = """DELETE FROM ratings WHERE id = %(rating_id)s"""
        data = {"rating_id": rating_id}
        connectToMySQL(Rating.DB).query_db(query, data)
        return
    
    @classmethod
    def has_submitted_rating(cls, pie_id, user_id):
        query = "SELECT COUNT(*) FROM ratings WHERE pie_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (pie_id, user_id))
        return result[0]['COUNT(*)'] > 0

    @classmethod
    def get_user_rating_id(cls, pie_id, user_id):
        query = "SELECT id FROM ratings WHERE pie_id = %s AND user_id = %s"
        result = connectToMySQL(cls.DB).query_db(query, (pie_id, user_id))
        if result:
            return result[0]['id']
        return None