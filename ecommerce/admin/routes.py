from flask import Blueprint, render_template, redirect, url_for, session, flash, g
from ecommerce.admin.forms import AdminLoginForm
from ecommerce.db import Database as db

admin = Blueprint('admin', __name__)

@admin.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@admin.route('/admin', methods=['GET', 'POST'])
def admin_login():
    '''Login controller for administrator'''
    form = AdminLoginForm()
    error = None

    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            # reconnect to heroku db
            db.reconnect()
            # retrieve the admin 
            cursor.execute('''SELECT * FROM admin WHERE username LIKE (%s)''', (form.username.data))
            
            # fetch user
            user = cursor.fetchone()
            session.pop('user', None)
        
        if user is None:
            # checks if user exists
            error = 'Username doesn\'t exists'

        elif not user['password']:
            # if the user does exist but the password doesn't match 
            error = 'Wrong password'

        else:
            # start session with the user (admin) and redirect to the admin page
            session['is_admin'] = True
            session['admin'] = user
            print(session)    
            return redirect(url_for('admin.admin_page', id=user['admin_id']))
            
        # flash message
        flash(error)

    return render_template('admin/login.html', form=form)

@admin.route('/admin/logout')
def logout():
    pass

@admin.route('/admin/<string:id>')
def admin_page(id):
    '''Overview all the tables - administrator page'''

    return render_template('admin/admin.html')

# admin list
@admin.route('/admin/list')
def admin_list():
    '''List of all the administrators'''
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
        # Select all administrators
        cursor.execute('SELECT * FROM admin')
        # fetch the result
        admin_list = cursor.fetchall()
    
    return render_template('admin/admin_list.html', admin_list=admin_list)

# customers list
@admin.route('/admin/customers')
def customer_list():
    '''List of all the customers'''
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
        # Select all customers
        cursor.execute('SELECT * FROM user ORDER BY joined_on ASC')
        customer_list = cursor.fetchall()

    return render_template('admin/customer_list.html', customer_list=customer_list)

# address, country, city list
@admin.route('/admin/addresses')
def address_list():
    '''List of all address'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
        
        # select all addresses
        cursor.execute('SELECT * FROM address')

        # fetch all
        address_list = cursor.fetchall()
    
    return render_template('admin/address_list.html', address_list=address_list)

@admin.route('/admin/cities')
def city_list():
    '''List of all cities'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()

        # select all cities
        cursor.execute('SELECT * FROM city')

        # fetch results
        city_list = cursor.fetchall()

    return render_template('admin/city_list.html', city_list=city_list)

@admin.route('/admin/countries')
def country_list():
    '''List of all countries'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        cursor.execute('SELECT * FROM country')

        # fetch results
        country_list = cursor.fetchall()

    return render_template('admin/country_list.html', country_list=country_list)

# category list
@admin.route('/admin/categories')
def category_list():
    '''List of all the categories'''
    
    return render_template('admin/category_list.html')

# product list
@admin.route('/admin/products')
def product_list():
    '''List of all the products sorted by store owner'''

    return render_template('admin/product_list.html')

# store list
@admin.route('/admin/stores')
def store_list():
    '''List of all the stores'''

    return render_template('admin/store_list.html')

