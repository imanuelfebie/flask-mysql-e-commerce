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


class AddressCreateForm(FlaskForm):
    '''Add address to the user object''' 
    line1 = StringField('address 1', validators=[DataRequired()])
    line2 = StringField('address 2') # not required field
    line3 = StringField('address 3') # not required field
    postal_code = StringField('postal code', validators=[DataRequired()])
    city = SelectField('city', coerce=int)
    user_id = HiddenField()
    submit = SubmitField('Submit') 

class ProfileUpdateForm(FlaskForm):
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    email = StringField('email')    
    submit = SubmitField('update')

class AddressUpdateForm(FlaskForm):
    address_line1 = StringField('address line 1')
    address_line2 = StringField('address line 2')
    address_line3 = StringField('address line 3')
    postal_code = StringField('postal code')
    city = SelectField('city', coerce=int)
    submit = SubmitField('update')


class UserUpdateForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    submit = SubmitField('Update')


class UserPasswordUpdateForm(FlaskForm):
    new_password1 = PasswordField('new password', validators=[DataRequired()])
    new_password2 = PasswordField('confirm new password', validators=[DataRequired(), EqualTo('new_password1')])
    submit = SubmitField('Update')   

#class AddressUpdateForm(FlaskForm):
#    line1 = StringField('address 1')
#    line2 = StringField('address 2') # not required field
#    line3 = StringField('address 3') # not required field
#    postal_code = StringField('postal code')
#    country = SelectField('country', coerce=int)
#    city = SelectField('city', coerce=int)
#    user_id = HiddenField()
#    submit = SubmitField('Submit')
