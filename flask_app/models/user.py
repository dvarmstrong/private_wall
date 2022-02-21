
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User :

    db_name = 'private_wall'
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.name =[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"

        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod 
    def get_by_email(cls,data):
        query =  "SELECT  * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users ;"
        results = connectToMySQL(cls.db_name).query_db(query)

        all_users = []
        for row in results:
            users_obj = cls(row)
            print(results)
            all_users.append(users_obj)
        return all_users

    @classmethod 
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])




    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Invalid First Name", "register")
            is_valid = False
        if len(user['last_name']) < 2 :
            flash("Invalid Last Name", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        # if not EMAIL_REGEX.match(User.get_by_email()):
        #     flash("Email already taken", "login")
        #     is_valid = False
        if len(user['password']) < 8:
            flash("Invalid Password", "Register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash ("Passwords do not match", "register")
            is_valid = False
        return is_valid








        
        
        
