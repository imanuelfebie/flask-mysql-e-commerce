from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from ecommerce.admin.forms import (AdminLoginForm, AdminCreateForm, AdminUpdateForm,
                                   CityForm, CityUpdateForm, CountryForm, 
                                   CountryUpdateForm, CategoryForm, ProductCreateForm, 
                                   ProductUpdateForm, StoreCreateForm, StoreUpdateForm, 
                                   CustomerCreateForm, PaymentMethodForm)
from ecommerce.users.forms import UserUpdateForm, AddressCreateForm
from ecommerce.store.forms import StoreRegistrationForm
from ecommerce.db import Database as db

admin = Blueprint('admin', __name__)

@admin.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

# admin decorator
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized to access the page.')
            return redirect(url_for('admin.admin_login'))
    return wrap


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

        elif not user['password'] == form.password.data:
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
    # release session variable
    session.pop('admin', None)
    session.pop('is_admin', False)
    
    print(session)

    return redirect(url_for('admin.admin_login'))

@admin.route('/admin/<string:id>')
@is_admin
def admin_page(id):
    '''Overview all the tables - administrator page'''
    
    with db.connection.cursor() as cursor:
        db.reconnect()
        # count all customer;
        cursor.execute("SELECT COUNT(user_id) AS total_users FROM user")    
        total_users = cursor.fetchone()

        # count all stores
        cursor.execute("SELECT COUNT(store_id) AS total_stores FROM store")
        total_stores = cursor.fetchone()

        # count all products
        cursor.execute("SELECT COUNT(product_id) AS total_products FROM product")
        total_products = cursor.fetchone()

    return render_template('admin/admin.html', total_users=total_users['total_users'],
                            total_stores=total_stores['total_stores'],
                            total_products=total_products['total_products'])


#######################################################################
# ROUTES FOR RETRIEVING, CREATING, UPDATING AND DELETING ADMINISTRATORS

# admin list
@admin.route('/admin/list')
@is_admin
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

@admin.route('/admin/new', methods=['GET', 'POST'])
@is_admin
def admin_create():
    '''Create new administrator'''
    form = AdminCreateForm()
    
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            # reconnect to heroku
            db.reconnect()
            # insert new administrator
            cursor.execute('INSERT INTO admin (username, email, password) VALUES (%s, %s, %s)', (
                            form.username.data,
                            form.email.data,
                            generate_password_hash(form.password1.data)))
            # commit changes to database
            db.connection.commit()
            
            flash('new administrator has been added')
            
            return redirect(url_for('admin.admin_list'))

    return render_template('admin/admin_create.html', form=form)

@admin.route('/admin/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def admin_update(id):
    '''Update selected administrator'''
    form = AdminUpdateForm()


    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # retrieve selected admin data
        cursor.execute('SELECT * FROM admin WHERE admin_id=%s', int(id))
        admin = cursor.fetchone()
    
        # populate fields
        form.username.data = admin['username']
        form.email.data = admin['email']

        if form.validate_on_submit():
            # UPDATE admin
            cursor.execute("UPDATE admin SET username = %s, email = %s, password1 = %s, password2 = %s WHERE admin_id = %s", (
                            request.form['username'],
                            request.form['email'],
                            form.password1.data,
                            form.passord2.data,
                            id))
            db.connection.commit()

            return redirect(url_for('admin.admin_list'))

    return render_template('admin/admin_update.html', form=form, admin=admin)

@admin.route('/admin/delete/<string:id>')
@is_admin
def admin_delete(id):
    '''Delete selected administrator'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # delete from admin
        cursor.execute('DELETE FROM admin WHERE admin.admin_id=(%s)', (int(id)))
        # commit changes
        db.connection.commit()
        
        flash('Administrator has been deleted')

        return redirect(url_for('admin.admin_list'))


##########################################################################
# ROUTES FOR RETRIEVING, CREATING, UPDATING AND DELETING USERS (CUSTOMERS)


@admin.route('/admin/customers')
@is_admin
def customer_list():
    '''List of all the customers'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
        # Select all customers
        cursor.execute('SELECT u.user_id, u.firstname, u.lastname, u.email, u.joined_on, u.is_active, s.store_name FROM user u LEFT JOIN store s ON u.store_id=s.store_id ORDER BY u.joined_on DESC')
        customer_list = cursor.fetchall()

    return render_template('admin/customer_list.html', customer_list=customer_list)

@admin.route('/admin/customers/new', methods=['GET', 'POST'])
@is_admin
def customer_create():
    '''Create new user'''
    form = CustomerCreateForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
    
        # get all the cities
        cursor.execute('SELECT * FROM city')
        city_list = cursor.fetchall()
        form.city.choices = [(city['city_id'], city['name']) for city in city_list]

        if form.validate_on_submit():
            # insert into user first
            cursor.execute('INSERT INTO user (firstname, lastname, email, password, is_active) VALUES (%s, %s, %s, %s, %s)', (
                            form.firstname.data,
                            form.lastname.data,
                            form.email.data,
                            generate_password_hash(form.password1.data),
                            True
                            ))
            db.connection.commit()

            # select this user
            #cursor.execute('SELECT user_id FROM user WHERE email LIKE (%s)', (
            #                form.email.data))
            #user = cursor.fetchone()

            cursor.execute('INSERT INTO address (line1, line2, line3, postal_code, city_id) VALUES (%s, %s, %s, %s, %s)', (
                            form.address_line1.data,
                            form.address_line2.data,
                            form.address_line3.data,
                            form.postal_code.data,
                            form.city.data))
            db.connection.commit()

            cursor.execute('SELECT address_id FROM address WHERE line1=%s', (
                            form.address_line1.data))
            address = cursor.fetchone()

            cursor.execute('UPDATE user SET address_id=%s', (
                            address['address_id']))
            
            ## insert address into customer_view
            #cursor.execute('UPDATE customer_view SET address_line1=%s, address_line2=%s, address_line3=%s, postal_code=%s, city_id=%s WHERE user_id=%s', (
            #                form.address_line1.data,
            #                form.address_line2.data,
            #                form.address_line3.data,
            #                form.postal_code.data,
            #                form.city.data,
            #                user['user_id']))

            db.connection.commit()           
        
            flash(f'{form.firstname.data} {form.lastname.data} created')

            return redirect(url_for('admin.customer_list'))

    return render_template('admin/customer_create.html', form=form)

@admin.route('/admin/customer/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def customer_update(id):
    '''Update existing customer'''
    form = UserUpdateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku    
        db.reconnect()

        # retrieve selected user
        cursor.execute('SELECT firstname, lastname, email FROM user WHERE user_id=%s', (id))
        customer = cursor.fetchone()
        
        # populate fields with current data
        form.firstname.data = customer['firstname']
        form.lastname.data = customer['lastname']
        form.email.data = customer['email']

        if form.validate_on_submit():
            # Update customer
            cursor.execute('UPDATE user SET firstname=%s, lastname=%s, email=%s WHERE user_id=%s', (
                            request.form['firstname'],
                            request.form['lastname'],
                            request.form['email'],
                            id))
            # commit to db
            db.connection.commit()

            flash('Customer updated')
            print(form.errors)

            return redirect(url_for('admin.customer_list'))

    return render_template('admin/customer_update.html', form=form, customer=customer)

@admin.route('/admin/customer/delete/<string:id>')
@is_admin
def customer_delete(id):
    '''Delete selected customer from db'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # delete 
        cursor.execute('DELETE FROM user WHERE user_id=%s', (id))
        # commmit changes
        db.connection.commit()

        flash('Customer deleted')

        return redirect(url_for('admin.customer_list'))


##################################################################
# ROUTES FOR RETRIEVING, CREATING, UPDATING AND DELETING ADDRESSES


@admin.route('/admin/address/list')
@is_admin
def address_list():
    '''List of all address'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()
        
        # select all addresses
        cursor.execute('SELECT * FROM address_view')

        # fetch all
        address_list = cursor.fetchall()
    
    return render_template('admin/address_list.html', address_list=address_list)

@admin.route('/admin/address/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def address_update(id):
    '''Add a new address'''
    form = AddressCreateForm()

    with db.connection.cursor() as cursor:
        # recconect to heroku
        db.reconnect()
        # get selected address date
        cursor.execute('SELECT line1, line2, line3, postal_code, city_id FROM address WHERE address_id = %s', (id))
        # get address
        address = cursor.fetchone() 
        
        # get all cities for select form
        cursor.execute('''SELECT city_id, name FROM city''')
        city_list = cursor.fetchall()
        form.city.choices = [(city['city_id'], city['name']) for city in city_list]

        # populate fields
        form.line1.data = address['line1']
        form.line2.data = address['line2']
        form.line3.data = address['line3'] 
        form.postal_code.data = address['postal_code']
        #form.city.data = address['city_id']
        #form.country.data = address['country_id']
        
        print(form.city.data)
        print(type(address['city_id']))

        if form.validate_on_submit():
            # Update selected address
            cursor.execute("UPDATE address SET line1 = %s, line2 = %s, line3 = %s, postal_code = %s, city_id = %s WHERE address_id = %s", (
                            request.form['line1'],
                            request.form['line2'],
                            request.form['line3'],
                            request.form['postal_code'],
                            form.city.data,
                            id))  
            #commit to db
            db.connection.commit
            
            flash('Address updated')

            return redirect(url_for('admin.address_list'))   

    return render_template('admin/address_update.html', form=form)

#@admin.route('/admin/address/delete/<string:id>')
#@is_admin
#def address_delete(id):
#    '''Delete selected address'''
#    
#    with db.connection.cursor() as cursor:
#        # reconnect to heroku
#        db.reconnect()
#        # Delete selected address
#        cursor.execute('DELETE FROM address WHERE address_id = %s', (id))
#        # commit
#        db.connection.commit()
#
#    return redirect(url_for('admin.address_list'))


#############################################################
# ROUTES FOR CREATING, RETRIEVING, UPDATE AND DELETING CITIES 


@admin.route('/admin/cities')
@is_admin
def city_list():
    '''List of all cities'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku server
        db.reconnect()

        #cursor.execute('')

        # select all cities
        cursor.execute('SELECT city.city_id, city.name, country.name AS country_name FROM city INNER JOIN country ON city.country_id=country.country_id ORDER BY city.name ASC')

        # fetch results
        city_list = cursor.fetchall()

    return render_template('admin/city_list.html', city_list=city_list)

@admin.route('/admin/city/new', methods=['GET', 'POST'])
@is_admin
def city_create():
    form = CityForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # get countries
        cursor.execute('SELECT * FROM country')
        # fetch results
        country_list = cursor.fetchall()
        # select field for countries
        form.country.choices = [(country['country_id'], country['name']) for country in country_list]

        if form.validate_on_submit():
            cursor.execute("INSERT INTO city (name, country_id) VALUES (%s, %s)", (form.name.data, form.country.data))
            # commit to db
            db.connection.commit()

            flash('City has been added')

            return redirect(url_for('admin.city_list'))
        
    return render_template('admin/city_create.html', form=form)

@admin.route('/admin/city/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def city_update(id):
    '''Update city'''
    form = CityUpdateForm()

    with db.connection.cursor() as cursor:
        db.reconnect()
        # get current city
        cursor.execute("SELECT city.name, city.country_id, country.name AS country_name FROM city "
                       "INNER JOIN country ON city.country_id=country.country_id "
                       "WHERE city.city_id=%s", (id))
        city = cursor.fetchone()

        # get countries
        cursor.execute('SELECT * FROM country')
        # fetch results
        country_list = cursor.fetchall()
        # select field for countries
        form.country.choices = [(country['country_id'], country['name']) for country in country_list]

        # populate the fields with existing data
        form.name.data = city['name']
        form.country.data = city['country_id']

        if form.validate_on_submit():
            # 
            cursor.execute("UPDATE city SET name = %s, country_id = %s WHERE city_id = %s", (
                            request.form['name'],
                            request.form['country'],
                            id))
            db.connection.commit()

            flash('City has beed updated')

            return redirect(url_for('admin.city_list'))

    return render_template('admin/city_update.html', form=form)


#@admin.route('/admin/city/delete/<string:id>')
#@is_admin
#def city_delete(id):
#    '''Deleted selected city'''
#
#    with db.connection.cursor() as cursor:
#        # reconnect to heroku
#        db.reconnect()
#        # delete select city
#        cursor.execute("DELETE FROM city WHERE city_id=%s", (id))
#        db.connection.commit()
#        
#        flash('City has been deleted')
#
#        return redirect(url_for('admin.city_list'))


################################################################
# ROUTES FOR CREATING, RETRIEVING, UPDATING & DELETING COUNTRIES


@admin.route('/admin/countries')
@is_admin
def country_list():
    '''List of all countries'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        cursor.execute('SELECT * FROM country')

        # fetch results
        country_list = cursor.fetchall()

    return render_template('admin/country_list.html', country_list=country_list)

@admin.route('/admin/country/new', methods=['GET', 'POST'])
@is_admin
def country_create():
    '''Create country'''
    form = CountryForm()

    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            # reconnect to heroku
            db.reconnect()
            cursor.execute("INSERT INTO country (name) VALUES (%s)", (form.name.data))
            # commit to db
            db.connection.commit()

            flash('{} has been added'.format(form.name.data))

            return redirect(url_for('admin.country_list'))

    return render_template('admin/country_create.html', form=form)

@admin.route('/admin/country/update/<string:id>', methods=['POST', 'GET'])
@is_admin
def country_update(id):
    '''Update country'''
    form = CountryForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()

        # get country
        cursor.execute("SELECT name FROM country WHERE country_id=%s", (id))
        country = cursor.fetchone()

        # populate field
        form.name.data = country['name']
        
        if form.validate_on_submit():
            # update country
            cursor.execute("UPDATE country SET name = %s WHERE country_id=%s", (
                            request.form['name'],
                            id))
            db.connection.commit()

            flash('Update successfull')

            return redirect(url_for('admin.country_list'))

    return render_template('admin/country_update.html', form=form)

#@admin.route('/admin/country/delete/<string:id>')
#@is_admin
#def country_delete(id):
#    '''Delete selected Country'''
#
#    with db.connection.cursor() as cursor:
#        db.reconnect()
#        cursor.execute("DELETE FROM country WHERE country_id=%s", (id))
#        db.connection.commit()
#
#        flash('Delelete successfull')
#
#        return redirect(url_for('admin.country_list'))


#################################################################
# ROUTES FOR CREATING, RETRIEVING, UPDATING & DELETING CATEGORIES 

# category list
@admin.route('/admin/categories')
@is_admin
def category_list():
    '''List of all the categories'''
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # retrieve all categories
        cursor.execute('SELECT * FROM category')
        # fetch results
        category_list = cursor.fetchall()
    
    return render_template('admin/category_list.html', category_list=category_list)

@admin.route('/admin/category/new', methods=['GET', 'POST'])
@is_admin
def category_create():
    '''Create new category'''
    form = CategoryForm()

    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            # reconnect
            db.reconnect()

            cursor.execute("INSERT INTO category (category_name) VALUES (%s)", (form.name.data))
            # commit to db
            db.connection.commit()

            flash('category added')
            print(form.errors)

            return redirect(url_for('admin.category_list'))
    else:
        print(form.errors)
    
    return render_template('admin/category_create.html', form=form)
            
@admin.route('/admin/category/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def category_update(id):
    '''Updated selected category'''
    form = CategoryForm()
    with db.connection.cursor() as cursor:
        db.reconnect()
        # get category
        cursor.execute('SELECT category_name FROM category WHERE category_id=%s', (id))
        category = cursor.fetchone()

        # populate field
        form.name.data = category['category_name']
                         
        if form.validate_on_submit():
            cursor.execute("UPDATE category SET category_name = %s WHERE category_id = %s", (
                            request.form['name'],
                            id))
            db.connection.commit()

            flash('Category updated')

            return redirect(url_for('admin.category_list'))

    return render_template('admin/category_update.html', form=form)

#@admin.route('/admin/category/delete/<string:id>')
#@is_admin
#def category_delete(id):
#    '''Deleted selected category'''
#
#    with db.connection.cursor() as cursor:
#        db.reconnect()
#        # DELETE from category
#        cursor.execute("DELETE FROM category WHERE category_id=%s", (id))
#
#        flash('Delete successfull')
#
#        return redirect(url_for('admin.category_list'))


##############################################################
# ROUTES FOR CREATING, RETRIEVIN, UPDATING & DELETING PRODUCTS

# product list
@admin.route('/admin/products')
@is_admin
def product_list():
    '''List of all the products sorted by store owner'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # retrieve all products and order by the latest added on timestamp
        cursor.execute('SELECT p.product_id, p.name, p.price, p.added_on, s.store_name, c.category_name FROM product p '
                       'INNER JOIN category c ON c.category_id=p.category_id '
                       'INNER JOIN store s ON p.store_id=s.store_id ORDER BY p.added_on DESC')
        # fetch results
        product_list = cursor.fetchall()

    return render_template('admin/product_list.html', product_list=product_list)

@admin.route('/admin/product/new', methods=['GET', 'POST'])
@is_admin
def product_create():
    '''Create new product'''
    form = ProductCreateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect with heroku
        db.reconnect()
        
        # get categories
        cursor.execute("SELECT * FROM category")
        category_list = cursor.fetchall()
        # get stores
        cursor.execute("SELECT * FROM store")
        store_list = cursor.fetchall()

        # populate select field
        form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]
        form.store.choices = [(store['store_id'], store['store_name'])for store in store_list]

        if form.validate_on_submit():
            cursor.execute("INSERT INTO product (name, price, description, category_id, store_id) VALUES (%s, %s, %s, %s, %s)",(
                            form.name.data,
                            form.price.data,
                            form.description.data,
                            form.category.data,
                            form.store.data))
            # commit changes
            db.connection.commit()

            flash('Product added')

            return redirect(url_for('admin.product_list'))

    return render_template('admin/product_create.html', form=form)

@admin.route('/admin/product/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def product_update(id):
    '''Update selected product'''
    form = ProductUpdateForm() 

    with db.connection.cursor() as cursor:
        # reconnect with heroku
        db.reconnect()
        # get select product to update
        cursor.execute("SELECT name, price, description, category_id, store_id FROM product WHERE product_id = %s", (id))
        product = cursor.fetchone()

        # get categories
        cursor.execute("SELECT * FROM category")
        category_list = cursor.fetchall()

        # get stores
        cursor.execute("SELECT * FROM store")
        store_list = cursor.fetchall()

        # populate select field
        form.name.data = product['name']
        form.price.data = product['price']
        form.description.data = product['description']
        form.category.data = product['category_id']
        form.store.data = product['store_id']
        
        # select fields
        form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]
        form.store.choices = [(store['store_id'], store['store_name'])for store in store_list]

        if form.validate_on_submit():
            # update the selected product
            cursor.execute("UPDATE product SET name = %s, price = %s, description = %s, category_id = %s, store_id = %s WHERE product_id = %s", (
                            request.form['name'],
                            request.form['price'],
                            request.form['description'],
                            request.form['category'],
                            request.form['store'],
                            id))
            # commit changes
            db.connection.commit()

            flash('Product added')

            return redirect(url_for('admin.product_list'))

    return render_template('admin/product_update.html', form=form)

#@admin.route('/admin/product/delete/<string:id>')
#@is_admin
#def product_delete(id):
#    '''DELETE selected product'''
#
#    with db.connection.cursor() as cursor:
#        db.reconnect()
#        # delete from product
#        cursor.execute("DELETE FROM product WHERE product_id = %s", (id))
#        # commit changes
#        db.connection.commit()
#
#        flash('Delete successfull')
#
#        return redirect(url_for('admin.product_list'))

#############################################################
# ROUTES FOR CREATING, RETRIEVING, UDPATING & DELETING STORES 

# store list
@admin.route('/admin/stores')
@is_admin
def store_list():
    '''List of all the stores'''
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # retrieve all stores
        cursor.execute('''SELECT s.store_id, s.store_name, s.joined_on, concat(u.firstname, ' ', u.lastname) AS fullname FROM store s
                          INNER JOIN user u ON s.store_id=u.store_id 
                       ''')
        # fetch results
        store_list = cursor.fetchall()

    return render_template('admin/store_list.html', store_list=store_list)

@admin.route('/admin/store/new', methods=['GET', 'POST'])
@is_admin
def store_create():
    '''Create new store'''
    form = StoreCreateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # get users
        cursor.execute("SELECT user_id, concat(firstname, ' ', lastname) AS fullname FROM user")
        form.owner.choices = [(user['user_id'], user['fullname']) for user in cursor.fetchall()]
        
        if form.validate_on_submit():
            # insert storename and description into store table
            cursor.execute("INSERT INTO store (store_name, about) VALUES (%s, %s)", (form.name.data, form.about.data))
            # commit to db
            db.connection.commit()

            # select the store that just has been created
            cursor.execute("SELECT store_id FROM store WHERE store_name=%s", (
                             form.name.data))
            store = cursor.fetchone()
            
            # assign the store to the chosen user
            cursor.execute("UPDATE user SET store_id = %s WHERE user_id=%s", (
                            store['store_id'],
                            form.owner.data))
            # commit changes to db
            db.connection.commit()
            print(form.errors) 
            flash('Store added successfull')
            
            return redirect(url_for('admin.store_list'))
        print(form.errors)

    return render_template('admin/store_create.html', form=form)

@admin.route('/admin/store/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def store_update(id):
    '''Update selected store'''
    form = StoreUpdateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # get users
        cursor.execute("SELECT user_id, concat(firstname, ' ', lastname) AS fullname FROM user")
        user_list = cursor.fetchall()
        
        cursor.execute("SELECT store_name, about FROM store WHERE store_id=%s", (id))
        store = cursor.fetchone()

        # populate the select field witht the users
        form.owner.choices = [(user['user_id'], user['fullname']) for user in user_list]
        
        # populate fields
        form.name.data = store['store_name']
        form.about.data = store['about']

        
        if form.validate_on_submit():
            # insert storename and description into store table
            cursor.execute("UPDATE store SET store_name = %s, about = %s WHERE store_id = %s", (
                            request.form['name'],
                            request.form['about'],
                            id))
            # commit to db
            db.connection.commit()

            # assign the store to the chosen user
            cursor.execute("UPDATE user SET store_id = %s WHERE user_id=%s", (
                            id,
                            form.owner.data))
            # commit changes to db
            db.connection.commit()
            print(form.errors) 
            flash('Store added successfull')
            
            return redirect(url_for('admin.store_list'))
        print(form.errors)


    return render_template('admin/store_update.html', form=form)

@admin.route('/admin/payment-methods/new', methods=['GET', 'POST'])
@is_admin
def payment_method_create():
    '''Create new payment method'''
    form = PaymentMethodForm()

    with db.connection.cursor() as cursor:
        # heroku reconnect
        db.reconnect()
        # Insert into payment method
        if form.validate_on_submit():
            cursor.execute('INSERT INTO payment_method (payment_name) VALUES (%s)', (form.name.data)) 
            # commit insert to db
            db.connection.commit()

            #flash('Payment method has been added')

            return redirect(url_for('admin.payment_method_list'))

    return render_template('admin/payment_method_create.html', form=form)

@admin.route('/admin/payment-methods/delete/<string:id>')
@is_admin
def payment_method_delete(id):
    '''Delete selected payment method'''

    with db.connection.cursor() as cursor:
        db.reconnect()
        # delete from
        cursor.execute('DELETE FROM payment_method WHERE payment_method_id = %s', (id))
        # Commit changes

        return redirect(url_for('admin.payment_method_list'))

@admin.route('/amdin/payment-methods/update/<string:id>', methods=['GET', 'POST'])
@is_admin
def payment_method_update(id):
    form = PaymentMethodForm()

    with db.connection.cursor() as cursor:
        # heroku reconnect
        db.reconnect()

        cursor.execute('SELECT payment_name FROM payment_method WHERE payment_method_id = %s', (id))
        method = cursor.fetchone()
        
        form.name.data = method['payment_name']

        if form.validate_on_submit():
            # Update from
            cursor.execute('''UPDATE payment_method SET payment_name = %s WHERE payment_method_id = %s''', (
                              request.form['name'],
                              id))
            # commit update
            db.connection.commit()

            flash('Payment method updated')
            
            return redirect(url_for('admin.payment_method_list'))
            
    return render_template('admin/payment_method_update.html', form=form)

@admin.route('/admin/payment-methods/list')
@is_admin
def payment_method_list():
    '''List out the payment methods'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        # Retrieve all payment methods
        cursor.execute('SELECT payment_method_id AS id, payment_name AS name FROM payment_method')
        payment_method_list = cursor.fetchall()
        

    return render_template('admin/payment_method_list.html', payment_method_list=payment_method_list)


