from job_app import app
from job_app.controllers import users_controller, jobs_controller

if __name__ == '__main__':
    app.run(debug=True)