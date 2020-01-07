from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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


class StoreRegistrationForm(FlaskForm):
    '''Form to create a store'''
    name = StringField('store name', validators=[DataRequired()])
    description = TextAreaField('description')

    
