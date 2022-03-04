from job_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask import render_template, redirect, session,request
from job_app import app
from flask_bcrypt import Bcrypt
import re
from job_app.models import job

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = 'fav_jobs'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.jobs = []

    @classmethod 
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if not results:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def get_one_user(cls, data):        
        query = 'SELECT * FROM users WHERE users.id = %(id)s;'         
        results = connectToMySQL(cls.db_name).query_db(query, data)         
        if not results:              
            return False  
        else:             
            return cls(results[0])



    @classmethod
    def get_user_job(cls,data):
        query = "SELECT * FROM users LEFT JOIN jobs ON jobs.user_id=users.id WHERE users.id=%(id)s; "
        results = connectToMySQL(cls.db_name).query_db(query,data)
        user = cls(results[0])
        if results[0]['jobs.id']==None:
            return cls(results[0])
        else:
            for user_job in results:
                job_data ={
                'id': user_job['jobs.id'],
                'job_name': user_job['job_name'],
                'genre': user_job['genre'],
                'home_city': user_job['home_city'],
                'created_at': user_job['jobs.created_at'],
                'updated_at' : user_job['jobs.updated_at'],
                'users_id': user_job['user_id']
                }
                user.jobs.append(job.Job(job_data))
        return user
        

    @classmethod
    def register_user(cls,data):
        query= "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)



    @staticmethod
    def valid_registration(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        edata = {
            'email' : data['email']
        }
        user = User.get_one_by_email(edata)
        if user:
            flash('Email already in use')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last Name must be at least 2 characters')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash ('Password must match')
            is_valid = False 
        return is_valid


    @staticmethod
    def valid_login(data):
        is_valid = True
        edata = {
            'email' : data['email']
        }
        user = User.get_one_by_email(edata)
        
        if not user:
            is_valid = False
            flash('Invalid Input')

        elif not bcrypt.check_password_hash(user.password, data['password']):
            is_valid = False
            flash('Invalid Input')
        return is_valid 

    @staticmethod
    def valid_user(data):
        is_valid = True
        data
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last Name must be at least 2 characters')
            is_valid = False
        return is_valid

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name =%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at = NOW() WHERE users.id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
