from flask import render_template, redirect, url_for, Blueprint, g, session
from ecommerce.store.forms import StoreRegistrationForm
from ecommerce.db import Database as db

store = Blueprint('store', __name__)

@store.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@store.route('/store/<string:id>')
def store_detail(id):
    '''Display the store\'s name & owner'''

    with db.connection.cursor() as cursor:
        db.reconnect()
        # Inner join to get the the necessary data to display
        # the
        cursor.execute('''SELECT u.firstname, u.lastname, s.store_name
                          FROM user u
                          INNER JOIN store s
                          ON u.store_id=s.store_id
                          WHERE s.store_id = (%s)
                          ''', (id))
        # fetch the data
        owner = cursor.fetchone()

        # select this store's products
        cursor.execute('''SELECT p.product_id, p.name, p.description, p.price
                          FROM product p 
                          INNER JOIN store s ON p.store_id=s.store_id
                          WHERE p.store_id=%s''', (id))
        product_list = cursor.fetchall()
    
    return render_template("store_detail.html", owner=owner, product_list=product_list)

@store.route('/store/manager/<string:id>')
def store_manager(id):
    '''Display the store owner's products'''
    with db.connection.cursor() as cursor:
        db.reconnect()
        cursor.execute('''SELECT p.product_id, p.name, p.price, p.description, p.category_id, c.category_name FROM product p
                          INNER JOIN category c
                          ON p.category_id=c.category_id
                          WHERE p.store_id = (%s)''',(id))
        product_list = cursor.fetchall()

    return render_template('store_manager.html', product_list=product_list)

@store.route('/store/register/<string:id>', methods=['POST', 'GET'])
def store_register(id):
    form = StoreRegistrationForm()

    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            cursor.execute('INSERT INTO store (store_name, about) VALUES (%s, %s)', (
                form.name.data,
                form.about.data,
            ))
            cursor.connection.commit()

            cursor.execute('''SELECT store_id FROM store WHERE store_name=(%s) and about=(%s)''', (form.name.data,form.about.data))
            store = cursor.fetchone()

            cursor.execute('''UPDATE user SET store_id= (%s) WHERE user_id = (%s)''', (store['store_id'], id))
            db.connection.commit()

        return redirect(url_for('store.store_detail', id=store['store_id']))

    else:
        print(form.errors)
        print('Failed to create store')

    return render_template('store_registration.html', form=form)

@store.route('/store/manager/purchase_history/<string:id>')
def purchase_history(id):
    with db.connection.cursor() as cursor:
        db.reconnect()

        cursor.execute('CREATE VIEW purchase_history_store '
                       'AS SELECT p.name, oi.quantity, oi.total_price, pm.payment_name, u.firstname, u.lastname '
                       'FROM product p, order_item oi, payment_method pm, user u, transaction t '
                       'WHERE t.payment_method_id=pm.payment_method_id '
                       'AND t.order_item_id=oi.order_item_id '
                       'AND oi.product_id=p.product_id '
                       'AND t.user_id= u.user_id '
                       'AND t.store_id=(%s)',(id))

        db.connection.commit()

        cursor.execute('SELECT * FROM purchase_history_store')
        phs=cursor.fetchall()
        print(phs)

        cursor.execute('DROP VIEW purchase_history_store')

        db.connection.commit()

        return render_template('purchase_history_store.html', phs=phs)

