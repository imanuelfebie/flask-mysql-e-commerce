from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField, 
        BooleanField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdminLogin(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired])
    login = SubmitField('Login')

class UserLoginForm(FlaskForm):
    '''Form for a user to authenticate'''
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField('Login')


class UserRegistrationForm(FlaskForm):
    '''Fields for new user registration'''
    email = StringField('email', validators=[
        DataRequired(), 
        Email()])
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    password1 = PasswordField('password', validators=[DataRequired()]) 
    password2 = PasswordField('confirm password', validators=[
        DataRequired(),
        EqualTo('password1')])
    submit = SubmitField('Register')
    login = SubmitField('Login')

    # Need to add username validation - Checking wether user already exist or not
    # both username and email


class AddressCreateForm(FlaskForm):
    '''Add address to the user object''' 
    line1 = StringField('address 1', validators=[DataRequired()])
    line2 = StringField('address 2') # not required field
    line3 = StringField('address 3') # not required field
    country = SelectField('country', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StoreRegistrationForm(FlaskForm):
    '''Form to create a store'''
    name = StringField('name', validators=[DataRequired()])
    about = TextAreaField('about')
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Register')

    
