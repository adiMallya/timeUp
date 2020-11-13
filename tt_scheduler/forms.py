#TO HANDLE FORMS ON THE PAGE
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    email = StringField('Email address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')