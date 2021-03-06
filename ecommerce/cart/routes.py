from flask import Blueprint, render_template, redirect, url_for, session, g, flash, request
from ecommerce.db import Database as db
#from ecommerce.cart.shopping_cart import ShoppingCart
from ecommerce.cart.forms import ItemAddToCart, ClearCartForm, ChoosePaymentMethodForm

cart = Blueprint('cart', __name__)

@cart.route('/cart/add/<string:id>')
def item_add_to_cart(id):
    # empty shopping cart
    shopping_cart = {}

    if request.form.validate_on_submit():
        session['shopping_cart'] = shopping_cart
        

@cart.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@cart.route('/cart/', methods=['POST', 'GET'])
def shopping_cart():
    form = ClearCartForm()
    total_price = 0

    for i in session['cart_item']:
        print(i)

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
    form = ClearCartForm()
    cart_item = {}
    total_price = 0

    with db.connection.cursor() as cursor:
        # reconnect to heroku cleardb database
        db.reconnect()
        if 'cart_item' in session:

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
                session['cart_item'][name] = {'qty': 1, 
                                              'price': price, 
                                              'id': id}
                session.modified = True

            else:
                session['cart_item'][name]['price'] += price
                session['cart_item'][name]['qty'] += 1
                # session['cart_item'][name]['id'] =
                # session['cart_item'][name] = {'qty': 1, 'price': price}
                session.modified = True


            for i in session['cart_item']:
                total_price += (session['cart_item'][i]['price'])

        else:
            session['cart_item'] = cart_item
            # reconnect to heroku cleardb database
            # db.reconnect()
            # # get this product
            # cursor.execute('SELECT * FROM product WHERE product_id=(%s)', (id))
            # product = cursor.fetchall()
            # name = ''
            # price = 0
            #
            # for p in product:
            #     name = p['name']
            #     price = int(p['price'])
            #
            # # product_detail = [(p['name'], p['price']) for p in product]
            # # print(product_detail)
            # session['cart_item'][name] = {'qty': 1, 'price': price, 'id':id}
            # session.modified = True
            #
            # for i in session['cart_item']:
            #     total_price += (session['cart_item'][i]['price'])
    
        if form.is_submitted():
            session.pop('cart_item')

            return redirect(url_for('cart.cart_items', id=g.user['user_id']))
    
    return redirect(url_for('cart.shopping_cart'))

##@cart.route('/cart/payment/methods', methods=['GET', 'POST'])
#def choose_payment_method():
#    form = ChoosePaymentMethodForm()
#    total_price = 0
#    with db.connection.cursor() as cursor:
#        for i in session['cart_item']:
#            total_price += (session['cart_item'][i]['price'])
#        # reconenct
#        db.reconnect()
#
#        cursor.execute('SELECT * FROM payment_method')
#        payment_list = cursor.fetchall()
#        form.payment_method.choices = [(payment['payment_method_id'], payment['payment_name']) for payment in payment_list]
#
#
#
#        # get address of user
#        cursor.execute('SELECT u.firstname, u.lastname, u.email, a.line1, a.line2, a.line3, a.postal_code, city.name AS city_name, country.name AS country_name FROM user u '
#                       'INNER JOIN address a ON u.address_id=a.address_id '
#                       'INNER JOIN city ON city.city_id=a.city_id '
#                       'INNER JOIN country ON city.country_id=country.country_id '
#                       'WHERE u.user_id=%s', (g.user['user_id']))
#        customer = cursor.fetchone()
#
#        cursor.execute('SELECT * FROM payment_method')
#        payment_list = cursor.fetchall()
#
#        form.payment_method.choices = [(p['payment_method_id'], p['payment_name']) for p in payment_list]
#
#        if form.is_submitted():
#            ts = time.time()
#            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#            # INSERT cart items into order item table
#            cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (
#                g.user['user_id']))
#            db.connection.commit()
#
#            print(g.user['user_id'])
#            cursor.execute("SELECT order_id FROM orders WHERE user_id= %s ORDER BY user_id DESC LIMIT 1", (g.user['user_id']))
#            order_id = cursor.fetchall()
#
#            for i in session['cart_item']:
#
#                # print (session['cart_item'][i]['id'])
#
#                # product_id = ','.join(str(z) for z in session['cart_item'][i]['id'])
#                # qty = ','.join(str(z) for z in session['cart_item'][i]['qty'])
#                # price = ','.join(str(z) for z in session['cart_item'][i]['price'])
#                # print(product_id, qty, price)
#                # print(type(product_id), type(qty), type(price))
#
#                # for z in product_id:
#                #     product_id = int(z)
#                #
#                # print(type(product_id))
#
#
#                # print(session['cart_item'][i]['id'],session['cart_item'][i]['qty'],session['cart_item'][i]['price'])
#
#                cursor.execute("INSERT INTO order_item (product_id, quantity, total_price, order_id) VALUES (%s, %s, %s, %s)", (
#                                str(session['cart_item'][i]['id']),
#                                str(session['cart_item'][i]['qty']),
#                                str(session['cart_item'][i]['price']),
#                                order_id))
#                # commit insert until done
#                db.connection.commit()
#
#                session.pop('cart_item', None)
#
#            # select the order_item
#
#            # get the payment method and insert into the transaction
#            cursor.execute("INSERT INTO transaction (payment_method_id, user_id, ordered_on, order_id) VALUES (%s, %s, %s, %s)", (
#                            form.payment_method.data,
#                            g.user['user_id'],
#                            st,
#                            order_id))
#            db.connection.commit()
#
#            flash('Payment Successful')
#
#            return redirect(url_for('cart.choose_payment_method', id=g.user['user_id']))
#
#    return render_template('payment_method.html', customer=customer, form=form, total_price=total_price)

