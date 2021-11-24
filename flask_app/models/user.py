from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# from flask_app.models.plan import Plan

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.plans = []
        
    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL("health_db").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        user_db = connectToMySQL("health_db").query_db(query,data)

        if len(user_db) < 1:
            return False
        
        return cls(user_db[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        user_db = connectToMySQL("health_db").query_db(query,data)
        return cls(user_db[0])
    
    @staticmethod
    def validate_register(user):
        email_reg =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least three characters")
            is_valid = False

        if len(user["last_name"]) < 3:
            flash("Last name must be at least three characters")
            is_valid = False
        
        if not email_reg.match(user["email"]):
            flash("Invalid Email")
            is_valid = False
        
        if len(user["password"]) < 8:
            flash("Password must be at least eight characters in length")
            is_valid = False

        if user["password"] != user["confirm_password"]:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid

    @classmethod
    def user_plans(cls, data):
        query = "SELECT * FROM users LEFT JOIN plans on users.id = plans.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("health_db").query_db(query, data)
        print(results)
        user = cls(results[0])
        for row in results:
            n = {
                "id":row["plans.id"],
                "name": row["name"],
                "fitness": row["fitness"],
                "yoga": row["yoga"],
                "meditation": row["meditation"],
                "cold_shower":row["cold_shower"],
                "check_app": row["check_app"],
                "frequency":row["frequency"],
                "accountable":row["accountable"],
                "help":row["help"],
                "reminder":row["reminder"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            user.plans.append( Plan(n) )
        return user
    