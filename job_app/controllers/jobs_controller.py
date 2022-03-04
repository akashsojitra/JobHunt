from job_app import app
from flask import render_template, redirect, session,request
from flask import flash
from job_app.models.user import User
from job_app.models.job import Job


@app.route('/create/job')
def new_job():
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    data={
        'id': session['user_id']
    }
    user = User.get_one_user(data)
    return render_template('create_job.html', user=user)

@app.route('/create/job/new', methods=['POST'])
def create_job():
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    if not Job.validate_job(request.form):
        return redirect('/create/job')
    data ={
        'company_name' : request.form['company_name'],
        'position' : request.form['position'],
        'status' : request.form['status'],
        'follow_up' : request.form['follow_up'],
        'user_id' : session['user_id']
    }
    Job.save(data)
    return redirect('/jobs')


@app.route('/edit/<int:job_id>')
def edit_job(job_id):
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    data = {
        "id" : job_id
    }
    user_data = {
        "id": session['user_id']
    }
    job=Job.get_one_job(data)
    return render_template('edit_job.html',job=job, user=User.get_one_user(user_data))

@app.route('/updatejob/<int:job_id>', methods=['POST'])
def update_job(job_id):
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    if not Job.validate_job(request.form):
        return redirect(f'/edit/{job_id}')
    data ={
        'id': job_id,
        'company_name' : request.form['company_name'],
        'position' : request.form['position'],
        'status' : request.form['status'],
        'follow_up' : request.form['follow_up'],
        'user_id' : session['user_id']
    }
    Job.update(data)
    return redirect('/jobs')



@app.route('/delete/<int:job_id>')
def delete_job(job_id):
    if not 'user_id' in session:
        flash('User must be logged in at')
        return redirect('/')
    data = {
        'id': job_id
    }
    Job.delete(data)
    return redirect('/jobs')




