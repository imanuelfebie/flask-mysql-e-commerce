from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField, 
        BooleanField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


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

    # Need to add username validation - Checking wether user already exist or not
    # both username and email


class AddressRegisterForm(FlaskForm):
    '''Register the user address'''
    line1 = StringField('address 1', validators=[DataRequired()])
    line2 = StringField('address 2') # not required field
    line3 = StringField('address 3') # not required field
    city = SelectField('city', coerce=int)
    country = SelectField('country', choices=[])
    postal_code = StringField('postal code', validators=[DataRequired()])
    submit = SubmitField('Submit')    

class UserUpdateForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    submit = SubmitField('Update')


class UserPasswordUpdateForm(FlaskForm):
    new_password1 = PasswordField('new password', validators=[DataRequired()])
    new_password2 = PasswordField('confirm new password', validators=[DataRequired(), EqualTo('new_password1')])
    submit = SubmitField('Update')


class AddressCreateForm(FlaskForm):
    '''Add address to the user object''' 
    line1 = StringField('address 1', validators=[DataRequired()])
    line2 = StringField('address 2') # not required field
    line3 = StringField('address 3') # not required field
    postal_code = StringField('postal code', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    user_id = HiddenField()
    submit = SubmitField('Submit')    
