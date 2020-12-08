from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db, bcrypt
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            password=hashed_password)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('Successfully registered! You may now login.','success')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form)



@auth.route('/', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and bcrypt.check_password_hash(employee.password, form.password.data):
            # log employee in
            login_user(employee, remember=form.remember.data)

            if employee.is_admin:
                # direct to the dashboard page after login
                # return render_template('dashboard.html')
                return redirect(url_for('admin.dashboard'))
            else:
                # return render_template('account.html')
                return redirect(url_for('user.homepage'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.','danger')

    # load login template
    return render_template('auth/login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    # redirect to the login page
    return redirect(url_for('auth.login'))