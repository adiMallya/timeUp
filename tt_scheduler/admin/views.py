from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required 

from . import admin
from .forms import SubjectForm, ClassForm, ClassAssignForm, EmployeeAssignForm
from .. import db
from ..models import Employee, Subject, Class



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


# ------------------------------------------------------------------------------------------------#
#Employee views

@admin.route('/employees', methods = ['GET','POST'])
@login_required
def list_employees():
    check_admin()

    employees = Employee.query.order_by(Employee.f_name).all()
    return render_template('admin/employees/employees.html',employees=employees, zip=zip)


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    
    check_admin()

    employee = Employee.query.get_or_404(id)

    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        for sid in form.subjects.data :
            employee.subjects.append(Subject.query.get(sid))

        for cid in form.classes.data:  
            employee.classes.append(Class.query.get(cid))

        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a subject and class')

        return redirect(url_for('admin.list_employees'))
    
    return render_template('admin/employees/employee.html',
                            employee=employee, form=form)
# ------------------------------------------------------------------------------------------------#
#Room views

@admin.route('/rooms', methods = ['GET','POST'])
@login_required
def list_rooms():
    check_admin()
    return render_template('admin/rooms/rooms.html')


# ------------------------------------------------------------------------------------------------#
#Subject views

@admin.route('/subjects', methods = ['GET','POST'])
@login_required
def list_subjects():
    check_admin()

    subjects = Subject.query.order_by(Subject.type).all()
    return render_template('admin/subjects/subjects.html', subjects=subjects)


@admin.route('/subjects/add', methods = ['GET','POST'])
@login_required
def add_subject():

    check_admin()

    add_subject = True

    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(sname=form.name.data,
                          type=form.type.data,
                          teach_hrs=form.teaching_hrs.data,
                          learn_hrs=form.learning_hrs.data,
                          credits=form.creds.data)

        try:

            db.session.add(subject)
            db.session.commit()
            flash('You have successfully added a new subject.','success')
        except:
            flash('Error: subject already exists.')

        return redirect(url_for('admin.list_subjects'))

    return render_template('admin/subjects/subject.html', action='Add',
                            add_subject=add_subject, form=form)


@admin.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
   
    check_admin()

    add_subject = False

    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.sname = form.name.data
        subject.teach_hrs = form.teaching_hrs.data
        subject.learn_hrs = form.learning_hrs.data
        subject.credits = form.creds.data
        db.session.commit()
        flash('You have successfully edited the subject.','success')

        return redirect(url_for('admin.list_subjects'))

    form.name.data = subject.sname
    form.teaching_hrs.data = subject.teach_hrs 
    form.learning_hrs.data = subject.learn_hrs
    form.creds.data = subject.credits
    return render_template('admin/subjects/subject.html', action="Edit",
                           add_subject=add_subject, form=form,
                           subject=subject)


@admin.route('/subjects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    
    check_admin()

    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('You have successfully deleted the subject.')

    return redirect(url_for('admin.list_subjects'))
# ------------------------------------------------------------------------------------------------#
#Class views

@admin.route('/classes', methods = ['GET','POST'])
@login_required
def list_classes():
    check_admin()

    classes = Class.query.order_by(Class.cid).all()
    return render_template('admin/classes/classes.html', classes=classes)


@admin.route('/classes/add', methods = ['GET','POST'])
@login_required
def add_class():

    check_admin()

    add_class = True
    assign_subject = False

    form = ClassForm()
    if form.validate_on_submit():
        classs = Class(   cid=form.sem_sec.data,
                          strength=form.strength.data)

        try:
            db.session.add(classs)
            db.session.commit()
            flash('You have successfully added a new class.','success')
        except:
            flash('Error: class already exists.')

        return redirect(url_for('admin.list_classes'))

    return render_template('admin/classes/class.html', action='Add',
                            add_class=add_class, assign_subject=assign_subject,
                            form=form)


@admin.route('/classes/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_class(id):
    
    check_admin()

    assign_subject = True

    classes = Class.query.get_or_404(id)

    form = ClassAssignForm(obj=classes)
    if form.validate_on_submit():
        for sid in form.subjects.data :
            classes.subjects.append(Subject.query.get(sid))

        db.session.add(classes)
        db.session.commit()
        flash('You have successfully assigned a subject to the class')

        return redirect(url_for('admin.list_classes'))
    
    return render_template('admin/classes/class.html',
                            classes=classes,assign_subject=assign_subject, form=form)



@admin.route('/classes/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_class(id):
   
    check_admin()

    add_class = False
    assign_subject = False

    classes = Class.query.get_or_404(id)
    form = ClassForm(obj=classes)
    if form.validate_on_submit():
        classes.cid = form.sem_sec.data
        classes.strength = form.strength.data
        db.session.commit()
        flash('You have successfully edited the class.','success')

        return redirect(url_for('admin.list_classes'))

    form.sem_sec.data = classes.cid
    form.strength.data = classes.strength 
    return render_template('admin/classes/class.html', action="Edit",
                           add_class=add_class, assign_subject=assign_subject,
                           form=form,
                           classes=classes)


@admin.route('/classes/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_class(id):
    
    check_admin()

    classes = Class.query.get_or_404(id)
    db.session.delete(classes)
    db.session.commit()
    flash('You have successfully deleted the class.')

    return redirect(url_for('admin.list_classes'))
# ------------------------------------------------------------------------------------------------#
#Profile views

@admin.route('/account', methods = ['GET','POST'])
@login_required
def show_profile():
    check_admin()
    return render_template('admin/account.html')