from flask import Blueprint, render_template, redirect, url_for, session, g
from ecommerce.orders.forms import PaymentMethodForm
from ecommerce.users.routes import is_authenticated

from ecommerce.db import Database as db

orders = Blueprint('orders', __name__)

@orders.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@orders.route('/order/confirm', methods=['GET', 'POST'])
@is_authenticated
def order_confirm():
    form = PaymentMethodForm()
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()

        # get the current user data
        cursor.execute('SELECT * FROM customer_view')
        customer = cursor.fetchone()
          
        # get the payment methods
        cursor.execute('SELECT * FROM payment_method')
        payment_methods = cursor.fetchall()

        form.payment_method.choices = [(p['payment_method_id'], p['payment_name']) for p in payment_methods]
        
        if form.validate_on_submit():
            # insert into transaction and related tables
            cursor.execute("INSERT INTO transaction (payment_method, user_id) VALUES (%s, %s)", (
                            form.payment_method.data,
                            session['user'].user_id))    
            db.connection.commit()
            
            # select the transaction that belongs to this user
            cursor.execute('SELECT * FROM transaction WHERE user_id=%s', (
                            session['user'].user_id))
            transaction = cursor.fetch()

            return redirect(url_for('order_confirmed.html'))

    return render_template('order_confirm.html', form=form, customer=customer)
