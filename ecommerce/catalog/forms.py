from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length


class CategoryCreateForm(FlaskForm):

    name = StringField('category', validators=[DataRequired()])
    submit = SubmitField('New Category')


class ProductCreateForm(FlaskForm):

    name = StringField('product name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    stock = IntegerField('stock', validators=[DataRequired()]) 
    price = DecimalField('price', validators=[DataRequired()]) 
    available = BooleanField('available')
    category = SelectField('catagories')
    submit = SubmitField('Add')

