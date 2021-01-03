from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required 

from . import admin
from .forms import SubjectForm, ClassForm, RoomForm, SubjectAssignForm, RoomAssignForm, EmployeeAssignForm, InchargeAssignForm
from ..user.forms import EditProfileForm
from .. import db
from ..models import Employee, Subject, Class, Room
from ..scheduler import Section


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

    employees = Employee.query
    subjects = Subject.query
    classes = Class.query
    rooms = Room.query
    return render_template('admin/dashboard.html',
                            employees=employees,
                            subjects=subjects,
                            classes=classes,
                            rooms=rooms
                            )


@admin.route('/dashboard/table')
@login_required
def generate():
    check_admin()

    classes = db.session.query(Class).all()
    sec_id = [c.cid for c in classes]

    subjects = db.session.query(Subject).select_from(Subject).join(Subject.classes)

    subj_3 = subjects.filter_by(cid='3A').filter(Subject.type.like('C')).filter(~Subject.sname.like('%Lab'))
    subj_5 = subjects.filter_by(cid='5A').filter(Subject.type.like('C')).filter(~Subject.sname.like('%Lab'))
    subj_7 = subjects.filter_by(cid='7A').filter(Subject.type.like('C')).filter(~Subject.sname.like('%Lab'))

    sub_list = [[s.sid for s in subj_3],[s.sid for s in subj_5],[s.sid for s in subj_7]]
    maxsub_count = [[s.teach_hrs for s in subj_3],[s.teach_hrs for s in subj_5],[s.teach_hrs for s in subj_7]]
    sub_name = [[s.sname for s in subj_3],[s.sname for s in subj_5],[s.sname for s in subj_7]]
    
    for i in range(3):
        sub_list[i].append(50)
        maxsub_count[i].append(20)
        sub_name[i].append('Lab')  

        sub_list[i].append(100)
        maxsub_count[i].append(20)
        sub_name[i].append('Elec')

    #7th seme
    sub_list[2].append(200)
    maxsub_count[2].append(20)
    sub_name[2].append('Open Elec')

    sec = []
    j=0
    
    for i in range(9): #Calling constructor for each section
        sec.append(Section(sec_id[i], sub_list[j], maxsub_count[j], sub_name[j]))
        if i==2 or i==5:
            j+=1

    for i in range(9):
        sec[i].lab_allocater()

    for i in [0,3,6]:
        sec[i].ele(0)
    
    for i in range(9):
        sec[i].ele_allocator(0)
    
    sec[6].ele(1)
    for i in [6,7,8]:
        sec[i].ele_allocator(1)
        
    for i in range(9):
        sec[i].allocator()
    
    output = []
    for i in range(9):
        output.append(sec[i].mat_str)
    
    days = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat'}

    return render_template('admin/table.html', output=output, days=days, zip=zip)
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

    rooms = Room.query.order_by(Room.lab).all()
    return render_template('admin/rooms/rooms.html', rooms=rooms)

@admin.route('/room/add', methods = ['GET','POST'])
@login_required
def add_room():

    check_admin()

    add_room = True
    # assign_room = False

    form = RoomForm()
    if form.validate_on_submit():
        room = Room(rno = form.room.data,
                    capacity =  form.capacity.data,
                    lab = form.is_lab.data,
                    no_of_sys =  form.num_sys.data)

        try:
            db.session.add(room)
            db.session.commit()
            flash('You have successfully added a new class.','success')
        except:
            flash('Error: class already exists.')

        return redirect(url_for('admin.list_rooms'))

    return render_template('admin/rooms/room.html', action='Add',
                            add_room=add_room,
                            form=form)


@admin.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room(id):
   
    check_admin()

    add_room = False

    room = Room.query.get_or_404(id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.rno = form.room.data
        room.capacity = form.capacity.data
        room.lab = form.is_lab.data
        room.no_of_sys = form.num_sys.data
        db.session.commit()
        flash('You have successfully edited the subject.','success')

        return redirect(url_for('admin.list_rooms'))

    form.room.data = room.rno
    form.capacity.data = room.capacity
    form.is_lab.data = room.lab
    form.num_sys.data = room.no_of_sys
    return render_template('admin/rooms/room.html', action="Edit",
                           add_room=add_room, form=form,
                           room=room)


@admin.route('/rooms/assign/icharge/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_incharge(id):
    check_admin()

    assign_incharge = True

    room = Room.query.get_or_404(id)
    
    form = InchargeAssignForm(obj=room)
    if form.validate_on_submit():
        for eid in form.employee.data :
            room.incharge.append(Employee.query.get(eid))

        db.session.add(room)
        db.session.commit()
        flash('You have successfully assigned an incharge')

        return redirect(url_for('admin.list_rooms'))
    
    return render_template('admin/rooms/room.html',
                            assign_incharge=assign_incharge,
                            room=room,
                            form=form)


@admin.route('/rooms/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_room(id):
    
    check_admin()

    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('You have successfully deleted the subject.')

    return redirect(url_for('admin.list_rooms'))
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
        subject.type = form.type.data
        subject.teach_hrs = form.teaching_hrs.data
        subject.learn_hrs = form.learning_hrs.data
        subject.credits = form.creds.data
        db.session.commit()
        flash('You have successfully edited the subject.','success')

        return redirect(url_for('admin.list_subjects'))

    form.name.data = subject.sname
    form.type.data = subject.type
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
    assign_room = False


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
                            add_class=add_class,
                            assign_subject=assign_subject,
                            assign_room=assign_room,
                            form=form)


@admin.route('/classes/assign/subject/<id>', methods=['GET', 'POST'])
@login_required
def assign_subject(id):
    check_admin()

    assign_subject = True

    classes = Class.query.get_or_404(id)

    form = SubjectAssignForm(obj=classes)
    if form.validate_on_submit():
        for sid in form.subjects.data :
            classes.subjects.append(Subject.query.get(sid))

        db.session.add(classes)
        db.session.commit()
        flash('You have successfully assigned a subject to the class')

        return redirect(url_for('admin.list_classes'))
    
    return render_template('admin/classes/class.html',
                            classes=classes, assign_subject=assign_subject, form=form)


@admin.route('/classes/assign/room/<id>', methods=['GET', 'POST'])
@login_required
def assign_room(id):
    check_admin()

    assign_room = True

    classes = Class.query.get_or_404(id)

    form = RoomAssignForm(obj=classes)
    if form.validate_on_submit():
        for rno in form.rooms.data :
            classes.rooms.append(Room.query.get(rno))

        db.session.add(classes)
        db.session.commit()
        flash('You have successfully assigned a room to the class')

        return redirect(url_for('admin.list_classes'))
    
    return render_template('admin/classes/class.html',
                            classes=classes, assign_room=assign_room, form=form)


@admin.route('/classes/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    check_admin()

    add_class = False
    assign_subject = False
    assign_room = False

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
                           add_class=add_class,
                           assign_subject=assign_subject,
                           assign_room=assign_room,
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

    user = Employee.query.get_or_404(current_user.eid)
    form = EditProfileForm(obj=admin)
    if form.validate_on_submit():
        user.f_name = form.fname.data
        user.m_name = form.mname.data
        user.l_name = form.lname.data
        user.type = form.type.data
        user.workload = form.workload.data
        user.ph_no = form.phno.data
        db.session.commit()
        flash('Profile updated.','success')

        return redirect(url_for('admin.show_profile'))

    form.username.data = user.username
    form.email.data = user.email
    form.fname.data = user.f_name
    form.mname.data = user.m_name
    form.lname.data = user.l_name
    form.type.data = user.type
    form.workload.data = user.workload
    form.phno.data = user.ph_no
    return render_template('admin/account.html', form=form, user=user)