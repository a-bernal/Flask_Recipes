from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = "recipes"
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.made_on = data['made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name,description,instructions,under_30,made_on,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_30)s,%(made_on)s,%(user_id)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            recipe.creator = user.User(user_data)
            recipes.append(recipe)
        return recipes


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_recipe = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_recipe.creator = user.User(user_data)
        return this_recipe
    

    @classmethod
    def update(cls,data):
        query = """
                UPDATE recipes
                SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s ,
                under_30 = %(under_30)s,
                made_on = %(made_on)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if recipe['made_on'] == '':
            flash("Please input a valid date.")
            is_valid = False
        if 'under_30' not in recipe:
            flash("Under 30 min, Y/N ?")
            is_valid = False

        return is_valid


