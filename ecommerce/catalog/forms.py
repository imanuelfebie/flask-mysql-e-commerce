from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField, DecimalField, SelectField,
                HiddenField)
from wtforms.validators import DataRequired, Length


class CategoryCreateForm(FlaskForm):
    name = StringField('category', validators=[DataRequired()])
    submit = SubmitField('Add')
		

class ProductCreateForm(FlaskForm):

    name = StringField('product name', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    description = StringField('description', validators=[DataRequired()])
    store_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('Add')


class ProductUpdateForm(FlaskForm):
    name = StringField('name')
    price = DecimalField('price')
    category = SelectField('categories', coerce=int)
    description = StringField('description')
    submit = SubmitField('update')

