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
        cursor.execute('''SELECT u.firstname, u.lastname, s.name
                          FROM user u
                          INNER JOIN store s
                          ON u.store_id=s.store_id
                          WHERE s.store_id = (%s)
                          ''', (id))
        # fetch the data
        object = cursor.fetchone()
    
    return render_template("store_detail.html", object=object)

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
    
    '''NO CLUE YET ON HOW TO UPDATE THE CURRENT USER TO THIS STORE'''
    
    return render_template('store_registration.html', form=form)

