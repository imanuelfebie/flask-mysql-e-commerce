from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField, 
        BooleanField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdminLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')

