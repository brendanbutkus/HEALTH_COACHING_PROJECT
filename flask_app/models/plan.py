from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Plan:
    def __init__(self, data):
        print(data)
        self.id = data["id"]
        self.name = data['name']
        self.fitness = data['fitness']
        self.yoga = data['yoga']
        self.meditation = data['meditation'] 
        self.cold_shower = data['cold_shower']
        self.check_app = data["check_app"]
        self.frequency= data["frequency"]
        self.accountable = data["accountable"]
        self.help = data["help"]
        self.reminder = data["reminder"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls,data):
        # if Plan.validate_plan(data):
            query = "INSERT INTO plans (name, fitness, yoga, meditation, cold_shower, check_app, frequency, accountable, help, reminder, user_id, created_at, updated_at) VALUES (%(name)s, %(fitness)s, %(yoga)s, %(meditation)s, %(cold_shower)s,%(check_app)s, %(frequency)s, %(accountable)s, %(help)s, %(reminder)s, %(user_id)s, NOW(), NOW());"
            return connectToMySQL("health_db").query_db(query, data)
        # return False
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM plans, users WHERE plans.user_id = users.id;"
        return connectToMySQL("health_db").query_db(query)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM plans, users WHERE plans.id = %(plan_id)s and users.id = plans.user_id;"
        return connectToMySQL("health_db").query_db(query, data)
        

    @classmethod
    def edit_one(cls, data):
        query = "SELECT * FROM plans, users WHERE plans.id = %(plan_id)s and users.id = plans.user_id and users.id = %(user_id)s;"
        return connectToMySQL("health_db").query_db(query, data)
        

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM plans WHERE id = %(id)s and user_id = %(user_id)s"
        results = connectToMySQL("health_db").query_db(query,data)
        
    
    @classmethod
    def update(cls,data):
        query = "UPDATE plans SET name=%(name)s,fitness=%(fitness)s,yoga=%(yoga)s,meditation=%(meditation)s,cold_shower=%(cold_shower)s,check_app=%(check_app)s, frequency=%(frequency)s,accountable=%(accountable)s,help=%(help)s,reminder=%(reminder)s,updated_at=NOW() WHERE id = %(plan_id)s;"
        return connectToMySQL("cars_db").query_db(query,data)

    @staticmethod
    def validate_plan(plan):
        is_valid = True
        if len(plan["accountable"]) < 20:
            is_valid = False
            flash("Accountability section must be at least 20 characters")
        if len(plan["help"]) < 3:
            is_valid = False
            flash("Who can help you must be at least 3 characters")
        return is_valid
        