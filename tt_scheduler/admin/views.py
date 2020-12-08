from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required 

from . import admin
from .. import db
from ..models import Employee



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403) 

#Dashboard views

@admin.route('/dashboard')
@login_required
def dashboard():
    check_admin() 
    return render_template('admin/dashboard.html')


#Employee views

@admin.route('/employees', methods = ['GET','POST'])
@login_required
def list_employees():
    check_admin()

    employees = Employee.query.order_by(Employee.f_name).all()
    return render_template('admin/employees/employees.html',employees=employees)


#Room views

@admin.route('/rooms', methods = ['GET','POST'])
@login_required
def list_rooms():
    check_admin()
    return render_template('admin/rooms/rooms.html')


#Subject views

@admin.route('/subjects', methods = ['GET','POST'])
@login_required
def list_subjects():
    check_admin()
    return render_template('admin/subjects/subjects.html')


#Class views

@admin.route('/classes', methods = ['GET','POST'])
@login_required
def list_classes():
    check_admin()
    return render_template('admin/classes/classes.html')


#Profile views

@admin.route('/account', methods = ['GET','POST'])
@login_required
def show_profile():
    check_admin()
    return render_template('admin/account.html')