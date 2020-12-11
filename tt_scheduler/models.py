#TO DEFINE SCHEMA FOR THE DATABASE
from flask_login import UserMixin
from tt_scheduler import db, login_manager
from sqlalchemy.orm import synonym

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

#-----------------------------------------TEACHES RELATIONSHIP-------------------------------------------------------------------
EmployeeSubject = db.Table('emp_subj',
                            db.Column('eid', db.Integer, db.ForeignKey("employee.eid", ondelete="cascade"), primary_key=True),
                            db.Column('sid', db.Integer, db.ForeignKey("subject.sid", ondelete="cascade"), primary_key=True),
)

SubjectClass = db.Table('subj_class',
                        db.Column('sid', db.Integer, db.ForeignKey("subject.sid", ondelete="cascade"), primary_key=True),
                        db.Column('class', db.String, db.ForeignKey("class.cid", ondelete="cascade"), primary_key=True)
)

ClassEmployee = db.Table('class_emp',
                        db.Column('eid', db.Integer, db.ForeignKey("employee.eid", ondelete="cascade"), primary_key=True),
                        db.Column('class', db.String, db.ForeignKey("class.cid", ondelete="cascade"), primary_key=True)
)
#-----------------------------------------CONDUCTS RELATIONSHIP-------------------------------------------------------------------
RoomSubject = db.Table('room_subj',
                        db.Column('rno', db.Integer, db.ForeignKey("room.rno", ondelete="cascade"), primary_key=True),
                        db.Column('sid', db.Integer, db.ForeignKey("subject.sid", ondelete="cascade"), primary_key=True)
)

ClassRoom = db.Table('class_room',
                        db.Column('rno', db.Integer, db.ForeignKey("room.rno", ondelete="cascade"), primary_key=True),
                        db.Column('class', db.String, db.ForeignKey("class.cid", ondelete="cascade"), primary_key=True)
)
#--------------------------------------------------------------------------------------------------------------------------------

class Employee(UserMixin, db.Model):
    '''
    For employee 
    '''
    __tablemame__ = 'employees'

    eid = db.Column(db.Integer, primary_key=True)
    id = synonym('eid')

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    f_name = db.Column(db.String(60))
    m_name = db.Column(db.String(60))
    l_name = db.Column(db.String(60))
    type = db.Column(db.String(10))
    workload = db.Column(db.Integer)
    ph_no = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)

    subjects = db.relationship('Subject', 
                                secondary=EmployeeSubject,
                                backref=db.backref('employees', lazy='dynamic'))

    assist = db.relationship('Room', backref='employee', uselist=False)#1:1 relationship with rooms

    
def __repr__(self):
        return f'<Employee: {self.username}, {self.email}>'



class Subject(db.Model):
    '''
    For subjects relation
    '''
    __tablemame__ = 'subjects'

    sid = db.Column(db.Integer, primary_key=True)
    id = synonym('sid')
    sname = db.Column(db.String(20), unique=True,nullable=False)
    type = db.Column(db.String(10), nullable=False)
    teach_hrs = db.Column(db.Integer, nullable=False)
    learn_hrs = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer)
    
    classes = db.relationship('Class', 
                                secondary=SubjectClass,
                                backref=db.backref('subjects', lazy='dynamic')
                                )
    def __iter__(self):
        return iter([self.sid])

    def __repr__(self):
            return f'<Subject: {self.sname}>'    



class Class(db.Model):
    '''
    For sections relation
    '''
    __tablemame__ = 'classes'

    cid = db.Column(db.String(5), primary_key=True)
    strength = db.Column(db.Integer, nullable=False)
      
    employees = db.relationship('Employee', 
                                secondary=ClassEmployee,
                                backref=db.backref('classes', lazy='dynamic'))

    rooms = db.relationship('Room', 
                                secondary=ClassRoom,
                                backref=db.backref('classes', lazy='dynamic'))
    def __iter__(self):
        return iter([self.cid])

    def __repr__(self):
        return f'<Class: {self.cid}>'



class Room(db.Model):
    __tablemame__ = 'rooms'

    rno = db.Column(db.Integer, primary_key=True)
    lab = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer, nullable=False)
    no_of_sys = db.Column(db.Integer)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.eid'))

    subjects = db.relationship('Subject',
                                secondary=RoomSubject,
                                backref=db.backref('rooms', lazy='dynamic'))


    def __iter__(self):
        return iter([self.rno])

    def __repr__(self):
        return f'<Room: {self.rno}>'

