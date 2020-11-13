from flask import render_template, url_for, redirect, flash
from tt_scheduler import app
from tt_scheduler.forms import LoginForm
# from flask_login import login_user, current_user, logout_user, login_required

@app.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #(WIP) just for testing; more stuff to come after dB created; 
        if form.email.data == "admin@nmit.ac.in" and form.password.data == "password":
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('landing.html', form=form)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/rooms')
def room():
    return render_template('rooms.html')

@app.route('/emp')
def emp():
    return render_template('employee.html')

@app.route('/subjects')
def subj():
    return render_template('subjects.html')

@app.route('/class')
def section():
    return render_template('classes.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/logout')
def logout():
   return redirect(url_for('login'))

