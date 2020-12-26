from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Subject, Class, Room


class SubjectForm(FlaskForm):
    '''
    Form for admin to add or edit subjects
    '''

    name = StringField('Name', validators=[DataRequired()])
    type = SelectField(u'Type', choices=[('C','Core'),('E','Elective')],validators=[DataRequired()])
    teaching_hrs = IntegerField('Teaching hours', validators=[DataRequired()])
    learning_hrs = IntegerField('Learning hours', validators=[DataRequired()])
    creds = IntegerField('Credits')
    submit = SubmitField('Submit')


class ClassForm(FlaskForm):
    '''
    Form for admin to add or edit classes
    '''

    sem_sec = StringField('Class', validators=[DataRequired()])
    strength = IntegerField('Class strength', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoomForm(FlaskForm):
    '''
    Form for admin to add or edit classes
    '''

    room = StringField('Room No.', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    is_lab = BooleanField('Lab ?')
    num_sys = IntegerField('No. of systems', default=0)
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    '''
    Form for the admin to assign subjects and class to the employee
    '''
    subjects = QuerySelectField('Subject',query_factory=lambda: Subject.query.all(),
                               get_label="sname")
    classes = QuerySelectField('Class',query_factory=lambda: Class.query.all(),
                               get_label="cid")
    submit = SubmitField('Assign')


class SubjectAssignForm(FlaskForm):
    '''
    Form for the admin to assign subjects to the class
    '''
    subjects = QuerySelectField(query_factory=lambda: Subject.query.all(),
                               get_label="sname")
    submit = SubmitField('Submit')


class RoomAssignForm(FlaskForm):
    '''
    Form for the admin to assign room to the class
    '''
    rooms = QuerySelectField(query_factory=lambda: Room.query.all(),
                               get_label="rno")
    submit = SubmitField('Submit')