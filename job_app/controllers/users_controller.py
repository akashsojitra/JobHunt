from job_app.models.job import Job
from job_app import app
from flask import render_template, redirect, session,request
from job_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.valid_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect('/jobs')



@app.route('/login', methods=["POST"])
def login():
    if not User.valid_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    user = User.get_one_by_email(data)
    session['user_id'] = user.id
    return redirect ('/jobs')




@app.route('/jobs')
def dashboard():
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_one_user(data)
    jobs = Job.get_all_complete()
    return render_template('dashboard.html', user=user,jobs=jobs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile/<int:user_id>')
def show_user(user_id):
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    
    user_data = {
        "id": session['user_id']
    }
    user=User.get_one_user(user_data)
    return render_template('show.html',user=user)

@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    if not User.valid_user(request.form):
        return redirect(f'/profile/{user_id}')
    data ={
        'id': user_id,
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
    }
    User.update_user(data)
    print
    return redirect('/jobs')