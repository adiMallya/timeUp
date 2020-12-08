#TO DEFINE SCHEMA FOR THE DATABASE
from flask_login import UserMixin
from tt_scheduler import db, login_manager
from sqlalchemy.orm import synonym

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


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

    def __iter__(self):
        return iter([self.cid])

    def __repr__(self):
        return f'<Class: {self.cid}>'