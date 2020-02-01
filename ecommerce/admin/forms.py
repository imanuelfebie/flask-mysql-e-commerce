from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField, 
        BooleanField, TextAreaField, HiddenField, DecimalField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdminLoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class AdminCreateForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Submit')


class AdminUpdateForm(FlaskForm):
    username = StringField('username')
    email = StringField('email', validators=[Email])
    password1 = PasswordField('new password')
    password2 = PasswordField('confirm new password', validators=[EqualTo('password1')])
    submit = SubmitField('update')

class CustomerCreateForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])

    address_line1 = StringField('line 1', validators=[DataRequired()])
    address_line2 = StringField('line 2')
    address_line3 = StringField('line 3')
    postal_code = StringField('postal_code', validators=[DataRequired()])
    city = SelectField('city', coerce=int)

    password1 = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('confirm password', validators=[DataRequired(),
                                                              EqualTo('password1')])
    submit = SubmitField('submit')

class CityForm(FlaskForm):
    name = StringField('city name', validators=[DataRequired()])
    country = SelectField('countries', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class CityUpdateForm(FlaskForm):
    name = StringField('city name')
    country = SelectField('countries', coerce=int)
    submit = SubmitField('update')


class CountryForm(FlaskForm):
    name = StringField('country name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CountryUpdateForm(FlaskForm):
    name = StringField('country name')
    submit = SubmitField('update')


class CategoryForm(FlaskForm):
    name = StringField('category name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProductCreateForm(FlaskForm):
    name = StringField('product name', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    category = SelectField('categories', coerce=int)
    store = SelectField('stores', coerce=int)
    submit = SubmitField('submit')    


class ProductUpdateForm(FlaskForm):
    name = StringField('product name')
    price = DecimalField('price')
    description = TextAreaField('description')
    category = SelectField('categories', coerce=int)
    store = SelectField('stores', coerce=int)
    submit = SubmitField('submit')   


class StoreCreateForm(FlaskForm):
    name = StringField('store name', validators=[DataRequired()])
    about = TextAreaField('Store description', validators=[DataRequired()])
    owner = SelectField('Assing owner', coerce=int)
    submit = SubmitField('submit')


class StoreUpdateForm(FlaskForm):
    name = StringField('store name')
    about = TextAreaField('Store description')
    owner = SelectField('Assing owner', coerce=int)
    submit = SubmitField('submit')

class PaymentMethodForm(FlaskForm):
    name = StringField('payment method', validators=[DataRequired()])   
    submit = SubmitField('submit')


