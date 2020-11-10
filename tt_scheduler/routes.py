from flask import render_template, url_for
from tt_scheduler import app

@app.route('/')
@app.route('/home') #root page
def home():
    return render_template('index.html')

@app.route('/rooms')
def room():
    return render_template('rooms.html')

@app.route('/employee')
def emp():
    return render_template('employee.html')

@app.route('/subjects')
def subj():
    return render_template('subjectss.html')

@app.route('/classes')
def sections():
    return render_template('classes.html')
