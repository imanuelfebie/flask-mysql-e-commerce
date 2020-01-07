from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length
from ecommerce.catalog.models import Category, Product



class CategoryCreateForm(FlaskForm):

	name = StringField('category', validators=[DataRequired()])
	submit = SubmitField('New Category')
		
class ProductCreateForm(FlaskForm):

    name = StringField('product name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    stock = IntegerField('stock', validators=[DataRequired()]) 
    price = DecimalField('price', validators=[DataRequired()])
    #available = DecimalField('available', validators=[DataRequired()])
    available = BooleanField('available')
    category = SelectField('catagories', choices=[])
    submit = SubmitField('Add')

