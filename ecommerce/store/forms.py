from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField, 
        BooleanField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class StoreRegistrationForm(FlaskForm):
    '''Form to create a store'''
    name = StringField('name', validators=[DataRequired()])
    about = TextAreaField('about')
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Register')


