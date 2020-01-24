from flask import Blueprint, render_template, redirect, url_for, session, g, flash
from ecommerce.db import Database as db
from ecommerce.cart.forms import ClearCartForm
import pymysql



cart = Blueprint('cart', __name__)

@cart.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@cart.route('/cart/', methods=['POST', 'GET'])
def shopping_cart():
    form = ClearCartForm()
    total_price = 0

    if 'cart_item' in session:
        for i in session['cart_item']:
            total_price += (session['cart_item'][i]['price'])

    else:
        return redirect(url_for('cart.cart_items', id=g.user['user_id']))

    if form.is_submitted():
        session.pop('cart_item')
        return redirect(url_for('cart.cart_items', id=g.user['user_id']))

    return render_template('cart.html', form=form, total_price=total_price)

@cart.route('/cart/<string:id>', methods=['POST', 'GET'])
def cart_items(id):
    cart_item = {}
    form = ClearCartForm()
    total_price = 0
    # with db.connection.cursor() as cursor:
    #     cursor.execute('''INSERT INTO order_item (product_id, quantity, total_price) VALUES (%s, %s, %s)''',
    #                    (generate_password_hash(password_form.new_password1.data),
    #                     id))
    #     # save changes to db
    #     db.connection.commit()
    #
    #     # show success message and redirect to the same page
    #     flash('Cart has been updated')
    #     return redirect(url_for('cart.shopping_cart', id=g.user['user_id']))

    # with db.connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM product")
    #     product_list = cursor.fetchall()
    #     try:
    #         cursor.execute("SELECT * FROM product")
    #         product_list = cursor.fetchall()
    #     except (pymysql.OperationalError):
    #         db.reconnect()
    #         cursor.execute("SELECT * FROM product")
    #         product_list = cursor.fetchall()
    if 'cart_item' in session:
        with db.connection.cursor() as cursor:
            # reconnect to heroku cleardb database
            db.reconnect()
            # get this product
            cursor.execute('SELECT * FROM product WHERE product_id=(%s)', (id))
            product = cursor.fetchall()
            name = ''
            price = 0
            for p in product:
                name = p['name']
                price = int(p['price'])

            # product_detail = [(p['name'], p['price']) for p in product]
            # print(product_detail)
            if name not in session['cart_item']:
                session['cart_item'][name] = {'qty': 1, 'price': price}
                session.modified = True
            else:
                session['cart_item'][name]['price'] += price
                session['cart_item'][name]['qty'] += 1
                # session['cart_item'][name] = {'qty': 1, 'price': price}
                session.modified = True


            for i in session['cart_item']:
                total_price += (session['cart_item'][i]['price'])

    else:
        session['cart_item'] = cart_item
        # with db.connection.cursor() as cursor:
        #     # reconnect to heroku cleardb database
        #     db.reconnect()
        #     # get this product
        #     cursor.execute('SELECT * FROM product WHERE product_id=(%s)', (id))
        #     product = cursor.fetchall()
        #     name = ''
        #     price = 0
        #     for p in product:
        #         name = p['name']
        #         price = int(p['price'])
        #
        #     session['cart_item'][name] = {'qty': 1, 'price': price}
        #     session.modified = True
    #
    # return session['cart_item']


    if form.is_submitted():
        session.pop('cart_item')
        return redirect(url_for('cart.cart_items', id=g.user['user_id']))

    # print(session['cart_item'])


    # return render_template('cart.html',form=form, total_price=total_price)
    return redirect(url_for('cart.shopping_cart'))


