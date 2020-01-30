from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class ItemAddToCart(FlaskForm):
    quantity = SelectField('quantity', coerce=int)
    submit = SubmitField('add')

class PaymentMethodForm(FlaskForm):
    payment_method = SelectField('payment method', coerce=int)
    submit = SubmitField('Order')
