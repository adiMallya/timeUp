from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, BooleanField, HiddenField, SubmitField, ValidationError
from wtforms.validators import DataRequired,Email,EqualTo


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    mname = StringField('Middle Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    type = SelectField('Job Type', choices=[('Teaching','Teaching'),
                                            ('Non-teaching','Non-teaching')])
    workload = IntegerField('Workload', validators=[DataRequired()])
    phno = StringField('Ph.No', validators=[DataRequired()])
    submit = SubmitField('Save')