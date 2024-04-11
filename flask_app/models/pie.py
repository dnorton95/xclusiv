from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.rating import Rating



class Pie:
    DB = "pies_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.recipe = data["recipe"]
        self.filling = data["filling"]
        self.crust = data["crust"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"] 
        self.user = User.find_user_by_id(self.user_id)  

    @staticmethod
    def form_is_valid(pie_input_data):
        is_valid = True
        # Text Validator
        if len(pie_input_data["recipe"]) == 0:
            flash("Please enter recipe.")
            is_valid = False
        elif len(pie_input_data["recipe"]) < 3:
            flash("Recipe must be at least three characters.")
            is_valid = False

        if len(pie_input_data["filling"]) == 0:
            flash("Please enter filling.")
            is_valid = False
        elif len(pie_input_data["filling"]) < 3:
            flash("Filling field must be at least three characters.")
            is_valid = False

        if len(pie_input_data["crust"]) == 0:
            flash("Please enter crust.")
            is_valid = False
        elif len(pie_input_data["crust"]) < 3:
            flash("Crust field must be at least three characters.")
            is_valid = False


        return is_valid

    @classmethod
    def find_all_pies(cls):
        query = """SELECT * FROM pies JOIN users ON pies.user_id = users.id"""
        list_of_dicts = connectToMySQL(Pie.DB).query_db(query)

        pies = []
        for each_dict in list_of_dicts:
            pie = Pie(each_dict)
            pies.append(pie)
        return pies
    
    @classmethod
    def get_all_pies(cls):
        query = """
            SELECT pies.*, users.id as user_id, users.first_name, users.last_name
            FROM pies
            JOIN users ON pies.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        
        all_pies = []
        for result in results:
            pie_data = {
                "id": result["id"],
                "recipe": result["recipe"],
                "filling": result["filling"],
                "crust": result["crust"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
                "user_id": {
                }
            }
            pie = Pie(pie_data)
            all_pies.append(pie)
        
        return all_pies

    
    @classmethod
    def find_all_pies_with_users(cls):
        query = """SELECT * FROM pies JOIN users ON pies.user_id = users.id"""

        list_of_dicts = connectToMySQL(Pie.DB).query_db(query)

        pies = []
        for each_dict in list_of_dicts:
            pie = Pie(each_dict)
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
            pie.user = user
            pies.append(pie)
        return pies
    
    @classmethod
    def find_pie_by_id(cls, pies_id):
        """this method finds a pie by the ID"""
        query = """SELECT * FROM pies WHERE id = %(pies_id)s"""
        data = {"pies_id": pies_id}
        list_of_dicts = connectToMySQL(Pie.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        pie = Pie(list_of_dicts[0])
        return pie
    
    @classmethod
    def find_pie_by_id_with_user(cls, pies_id):
        """This method find a pie by the id and user by the record id"""
        query = """
            SELECT pies.*, users.*
            FROM pies
            JOIN users ON pies.user_id = users.id 
            WHERE pies.id = %(pies_id)s
        """

        data = {"pies_id": pies_id}
        list_of_dicts = connectToMySQL(Pie.DB).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        pie = Pie(list_of_dicts[0])
        user_input_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        pie.user = User(user_input_data)
        return pie


    
    @classmethod
    def new_pie(cls, pie_input_data):
        try:
            # Insert pie data into the pies table
            query_pie = """
            INSERT INTO pies
            (recipe, filling, crust, user_id)
            VALUES
            (%(recipe)s, %(filling)s, %(crust)s, %(user_id)s)
            """
            pies_id = connectToMySQL(cls.DB).query_db(query_pie, pie_input_data)

            return pies_id
        except Exception as e:
            # Handle the error
            print(f"An error occurred: {str(e)}")
            return None
        
    @classmethod
    def create(cls, form_data):
        query = """INSERT INTO pies
        (recipe, filling, crust, user_id)
        VALUES
        (%(recipe)s, %(filling)s, %(crust)s, 
        %(user_id)s)"""
        pie_id = connectToMySQL(Pie.DB).query_db(query, form_data)
        return pie_id
    
    @classmethod
    def update(cls, pies_id, pie_input_data):
        query = "UPDATE pies SET recipe = %(recipe)s, filling = %(filling)s, crust = %(crust)s WHERE id = %(pies_id)s;"
        data = {
            "pies_id": pies_id,
            "recipe": pie_input_data["recipe"],
            "filling": pie_input_data["filling"],
            "crust": pie_input_data["crust"],
        }
        connectToMySQL(Pie.DB).query_db(query, data)
    
    @classmethod
    def delete_by_id(cls, pie_id):
        query = "DELETE FROM pies WHERE id = %(pie_id)s"
        data = {"pie_id": pie_id}
        connectToMySQL(Pie.DB).query_db(query, data)
        return
    
    @classmethod
    def count_by_recipe(cls, recipe):
        query = """SELECT COUNT(recipe) AS "count"
        FROM pies WHERE recipe = %(recipe)s"""
        data = {"recipe": recipe}
        list_of_dicts = connectToMySQL(Pie.DB).query_db(query, data)
        print(list_of_dicts)
        return list_of_dicts[0]["count"]
    
    @classmethod
    def find_pies_by_user_id(cls, user_id):
        """Find pies associated with a specific user"""
        query = """
            SELECT pies.*, users.*
            FROM pies
            JOIN users ON pies.user_id = users.id 
            WHERE users.id = %(user_id)s
        """

        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(Pie.DB).query_db(query, data)

        pies = []
        for pie_data in list_of_dicts:
            pie = Pie(pie_data)

            user_input_data = {
                "id": pie_data["users.id"],
                "first_name": pie_data["first_name"],
                "last_name": pie_data["last_name"],
                "email": pie_data["email"],
                "password": pie_data["password"],
                "created_at": pie_data["users.created_at"],
                "updated_at": pie_data["users.updated_at"],
            }
            pie.user = User(user_input_data)
            pies.append(pie)

        return pies
    
    @classmethod
    def find_all_pies_with_users_and_ratings(cls):
        query = """
            SELECT 
                pies.*, 
                users.id AS user_id, 
                users.first_name, 
                users.last_name,
                ratings.id AS rating_id, 
                ratings.points, 
                ratings.pie_id,
                users.id AS user_id  -- Alias the users.id column
            FROM 
                pies
            JOIN 
                users ON pies.user_id = users.id
            LEFT JOIN 
                ratings ON pies.id = ratings.pie_id
            ORDER BY 
                pies.id, 
                ratings.created_at DESC

        """
        results = connectToMySQL(cls.DB).query_db(query)

        pies = []
        current_pie = None
        for result in results:
            if not current_pie or current_pie.id != result["id"]:
                current_pie = cls(result)
                current_pie.ratings = []  # Initialize ratings list for the current pie
                pies.append(current_pie)

            if result["rating_id"]:  # If there is a rating associated with the pie
                current_pie.ratings.append(Rating(result))  # Add the rating to the current pie's ratings list

        return pies

