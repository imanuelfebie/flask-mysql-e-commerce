from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, PasswordField, SubmitField,
        BooleanField, TextAreaField, HiddenField)
from wtforms.validators import DataRequired, Length, Email, EqualTo

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class ItemAddToCart(FlaskForm):
    quantity = SelectField('quantity', coerce=int)
    submit = SubmitField('add')

class ClearCartForm(FlaskForm):
    clear = SubmitField("CLEAR CART")

class ChoosePaymentMethodForm(FlaskForm):
    payment_method = SelectField('payment method', coerce=int)
    submit = SubmitField('Order')
