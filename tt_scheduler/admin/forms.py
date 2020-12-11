from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Subject, Class


class SubjectForm(FlaskForm):
    '''
    Form for admin to add or edit subjects
    '''

    name = StringField('Name', validators=[DataRequired()])
    type = SelectField(u'Type', choices=[('C','Core'),('E','Elective')],validators=[DataRequired()])
    teaching_hrs = IntegerField('Teaching hours', validators=[DataRequired()])
    learning_hrs = IntegerField('Learning hours', validators=[DataRequired()])
    creds = IntegerField('Credits')
    sumbit = SubmitField('Submit')


class ClassForm(FlaskForm):
    '''
    Form for admin to add or edit classes
    '''

    sem_sec = StringField('Class', validators=[DataRequired()])
    strength = IntegerField('Class strength', validators=[DataRequired()])
    sumbit = SubmitField('Submit')


class RoomForm(FlaskForm):
    '''
    Form for admin to add or edit classes
    '''

    room = StringField('Room No.', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    is_lab = BooleanField('Lab ?')
    num_sys = IntegerField('No. of systems', default=0)
    sumbit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    '''
    Form for the admin to assign subjects and class to the employee
    '''
    subjects = QuerySelectField(query_factory=lambda: Subject.query.all(),
                               get_label="sname")
    classes = QuerySelectField(query_factory=lambda: Class.query.all(),
                               get_label="cid")
    submit = SubmitField('Submit')


class ClassAssignForm(FlaskForm):
    '''
    Form for the admin to assign subjects to the class
    '''
    subjects = QuerySelectField(query_factory=lambda: Subject.query.all(),
                               get_label="sname")
    submit = SubmitField('Submit')

