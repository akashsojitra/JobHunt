from job_app.config.mysqlconnection import connectToMySQL
from flask import flash
from job_app import app
from job_app.models import user

class Job:
    db_name = 'fav_jobs'
    def __init__(self, data):
        self.id = data['id']
        self.company_name = data['company_name']
        self.position = data['position']
        self.status = data['status']
        self.follow_up = data['follow_up']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO jobs (company_name, position, status, follow_up, user_id,  created_at, updated_at) VALUES (%(company_name)s, %(position)s, %(status)s,  %(follow_up)s, %(user_id)s, NOW(), NOW());'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM jobs;"
        results = connectToMySQL(cls.db_name).query_db(query)
        new_jobs =[]
        if not results:
            return new_jobs
        
        for job in results:
            new_jobs.append(cls(job))
        return new_jobs
        
    @classmethod
    def get_all_complete(cls):
        query = "SELECT * FROM jobs JOIN users ON jobs.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        new_jobs =[]
        if not results:
            return new_jobs
        else:
            for job in results:
                user_data = {
                    'id' : job['users.id'],
                    'first_name': job['first_name'],
                    'last_name': job['last_name'],
                    'email' : job['email'],
                    'password' : job['password'],
                    'created_at': job['users.created_at'],
                    'updated_at': job['users.updated_at'],
                }
                creator = user.User(user_data)
                new_job = cls(job)
                new_job.creator = creator 
                new_jobs.append(new_job)
        return new_jobs

    @classmethod
    def get_one_job(cls, data):        
        query = 'SELECT * FROM jobs WHERE jobs.id = %(id)s;'         
        results = connectToMySQL(cls.db_name).query_db(query, data)         
        if not results:              
            return False  
        else:             
            return cls(results[0])

    

    @staticmethod
    def validate_job(data):
        is_valid = True
        data
        if len(data['company_name']) < 3:
            flash("Company Name must be at least 3 charactors")
            is_valid = False
        if len(data['position']) < 3:
            flash("Position must be at least 3 charactors")
            is_valid = False
        if len(data['status']) < 3:
            flash("Status must be at least 3 charactors")
            is_valid = False
        if len(data['follow_up']) < 3:
            flash("Follow Up must be at least 3 charactors")
            is_valid = False
        return is_valid



    @classmethod
    def update(cls,data):
        query = "UPDATE jobs SET company_name =%(company_name)s, position=%(position)s, status=%(status)s, follow_up=%(follow_up)s, updated_at = NOW() WHERE jobs.id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM jobs WHERE jobs.id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    

