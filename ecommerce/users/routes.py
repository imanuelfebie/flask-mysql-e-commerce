import pymysql
from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ecommerce.users.forms import (UserRegistrationForm, AddressRegisterForm, UserLoginForm, AddressCreateForm,
        UserUpdateForm, UserPasswordUpdateForm)
from ecommerce.db import Database as db
#from ecommerce import mysql

users = Blueprint('users', __name__)

# authentication decorator
def is_authenticated(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_authenticated' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthised page. Make sure you have the rights to view this page')
            return redirect(url_for('users.user_login'))
    return wrap

@users.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@users.route('/login', methods=['GET', 'POST'])
def user_login():
    '''Controller to authenticate a user and start a session'''
    form = UserLoginForm()
    error = None

    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            try:
                # retrieve user from the database where the email equals the input value
                cursor.execute('SELECT * FROM user WHERE email LIKE (%s)', (form.email.data))

                # fetch retreived user
                user = cursor.fetchone()
                session.pop('user', None)
                
            except (pymysql.OperationalError):
                # Reconnect first if an operationalError occures and repeat previous steps
                db.reconnect()
                cursor.execute('SELECT * FROM user WHERE email LIKE (%s)', (form.email.data)) 
                
                # fetch retreived user
                user = cursor.fetchone()
                session.pop('user', None)

            if user is None:
                # checks if user exists, if not display error message
                error = 'User doesn\'t exist'

            elif not check_password_hash(user['password'], form.password.data):
                #checks if password matches when user exists, if not displays error message
                error = 'Please insert correct username and password'

            else:
                # start new session with user, redirect to dashboard page
                session['is_authenticated'] = True
                session['user'] = user
                return redirect(url_for('users.account', id=user['user_id']))

            # display if any errors occur
            flash(error)

    return render_template('login.html', form=form)
    
@users.route('/logout')
@is_authenticated
def logout():
    '''Controller to logout users by ending clearing the session'''
    session.clear()
    return redirect(url_for('main.index'))


@users.route('/register', methods=['POST', 'GET'])
def register():
    '''Controller for registering new users'''
    
    form = UserRegistrationForm()
 
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            db.reconnect()
            # insert new user object into user
            cursor.execute('INSERT INTO user (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)', (
            form.firstname.data,
            form.lastname.data,
            form.email.data,
            generate_password_hash(form.password1.data)))

            # commit to db
            db.connection.commit()
        
        flash('Awesome! You just created an account and can now login')
        
        # redirect user to address form
        return redirect(url_for('users.user_login'))

    else:
        print(form.errors)
        print('Failed to insert new user to db')

    return render_template('register.html', form=form)

@users.route('/register/address/', methods=['GET','POST'])
def register_address():
    '''Controller to handle adding an address for new registered user'''

    form = AddressRegisterForm()
    
    with db.connection.cursor() as cursor:
        db.reconnect()
        cursor.execute('SELECT * FROM city,country WHERE country.name LIKE "indonesia"')
        city_list = cursor.fetchall()
        form.city.choices = [(city['city_id'],city['name']) for city in city_list]

        if form.validate_on_submit():
            with db.connection.cursor() as cursor:
                cursor.execute("INSERT INTO address (line1, line2, line3, postal_code, country)")
                db.connection.commit()

    return render_template('register_address.html', form=form)
    

@users.route('/profile/<string:id>')
@is_authenticated
def profile(id):
    '''render the user profile details'''

    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku mysql db
        db.reconnect()

        # get all the contries for select form
        cursor.execute('SELECT * FROM country')
        country_list = cursor.fetchall()
        address_form.country.choices = [(country['country_id'], country['name']) for country in country_list]
        
        # get all cities for select form
        cursor.execute('''SELECT city_id, name FROM city''')
        city_list = cursor.fetchall()
        address_form.city.choices = [(city['city_id'], city['name']) for city in city_list]

        # get address from current user
        cursor.execute('SELECT a.line1, a.line2, a.line3, a.postal_code, a.country_id, a.city_id FROM address a LEFT JOIN user u ON a.address_id=u.address_id WHERE u.user_id=(%s)', (id))
        user_address = cursor.fetchone()
        print(user_address['line1'])


    # Populate user detail fields
    profile_form.email.data = g.user['email']
    profile_form.firstname.data = g.user['firstname']
    profile_form.lastname.data = g.user['lastname']
    
    # populate address fields if address already filled
    address_form.line1.data = user_address['line1']
    address_form.line2.data = user_address['line2']
    address_form.line3.data = user_address['line3']
    address_form.postal_code.data = user_address['postal_code']
    address_form.country.data = user_address['country_id']
    address_form.city.data = user_address['city_id']

    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/profile/update/<string:id>', methods=['GET','POST'])
@is_authenticated
def profile_update(id):
    '''Controller to update the user's email, name, lastname'''

    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()
   
    if profile_form.validate_on_submit():
        with db.connection.cursor() as cursor:
            try:
                cursor.execute('''UPDATE user SET email = (%s), firstname = (%s), lastname = (%s) WHERE user_id = (%s)''', 
                                        (profile_form.email.data,
                                        profile_form.firstname.data,
                                        profile_form.lastname.data,
                                        id))
                # commit changes to database
                db.connection.commit()

            except (pymysql.OperationalError):
                db.reconnect()
            
        flash('Profile updated')
        return redirect(url_for('users.profile', id=g.user['user_id']))
    else:
        print(profile_form.errors)
        print("failed")
    
    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/profile/update/password/<string:id>', methods=['POST', 'GET'])
@is_authenticated
def password_update(id):
    '''Controller to handle the password update form'''

    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()


    if password_form.validate_on_submit():
        # Update the user password if the user passes the form validation
        with db.connection.cursor() as cursor:
            cursor.execute('''UPDATE user SET password = (%s) WHERE user_id = (%s)''',
                    (generate_password_hash(password_form.new_password1.data),
                    id))
            # save changes to db
            db.connection.commit()


            # show success message and redirect to the same page
            flash('Password has been updated')
            return redirect(url_for('users.profile', id=g.user['user_id']))
    else:
        flash('Something went wrong')
 
    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)


@users.route('/profile/update/address/<string:id>', methods=['GET', 'POST'])
@is_authenticated
def address_update(id):
    '''Controller to handle address update form'''

    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku mysql db
        db.reconnect()

        # get all the contries for select form
        cursor.execute('SELECT * FROM country')
        country_list = cursor.fetchall()
        address_form.country.choices = [(country['country_id'], country['name']) for country in country_list]
        
        # get all cities for select form
        cursor.execute('''SELECT city_id, name FROM city''')
        city_list = cursor.fetchall()
        address_form.city.choices = [(city['city_id'], city['name']) for city in city_list]


        if address_form.validate_on_submit():
            # insert address to database
            cursor.execute('''INSERT INTO address (line1, line2, line3, postal_code, country_id, city_id) VALUES (%s, %s, %s, %s, %s, %s)''', (
                           address_form.line1.data,
                           address_form.line2.data,
                           address_form.line3.data,
                           address_form.postal_code.data,
                           address_form.country.data,
                           address_form.city.data))
            # commit to db
            cursor.connection.commit()
            
            # get address id
            cursor.execute('''SELECT address_id FROM address WHERE line1=(%s)''', (address_form.line1.data))
            address = cursor.fetchone()
            
            # update address_id to currentuser
            cursor.execute('''UPDATE user SET address_id = (%s) WHERE user_id = (%s)''', (address['address_id'], id))
            db.connection.commit()
            
            flash('Address has beed added')

            return redirect(url_for('users.profile', id=g.user['user_id']))
        else:
            flash('{}'.format(address_form.errors))

    #with db.connection.cursor() as cursor:
    #    db.reconnect()
    #    cursor.execute('SELECT * FROM country')
    #    country_list = cursor.fetchall()
    #    address_form.country.choices = [(country['country_id'], country['name']) for country in country_list]
    #    with db.connection.cursor() as cursor:
    #        db.reconnect()
    #        cursor.execute('''SELECT city_id, name FROM city''')
    #        city_list = cursor.fetchall()
    #        address_form.city.choices = [(city['city_id'], city['name']) for city in city_list]


    #if address_form.validate_on_submit():
    #    with db.connection.cursor() as cursor:
    #        cursor.execute('''INSERT INTO address (line1, line2, line3, postal_code, country_id, city_id) VALUES (%s, %s, %s, %s, %s, %s)''',
    #                       (address_form.line1.data,
    #                        address_form.line2.data,
    #                        address_form.line3.data,
    #                        address_form.postal_code.data,
    #                        address_form.country.data,
    #                        address_form.city.data
    #                        ))
    #        # save changes to db
    #        db.connection.commit()
    #        with db.connection.cursor() as cursor:
    #            cursor.execute(
    #                'SELECT address_id FROM address WHERE line1 = (%s)',
    #                (address_form.line1.data
    #                 ))
    #            address_list = cursor.fetchall()
    #            address_id = [(address['address_id']) for address in address_list]
    #            with db.connection.cursor() as cursor:
    #                cursor.execute(
    #                    '''UPDATE user SET address_id = (%s) WHERE user_id = (%s)''',
    #                    (address_id,
    #                     id
    #                     ))
    #                db.connection.commit()

    #                # show success message and redirect to the same page
    #                flash('Address has been updated')
    #                return redirect(url_for('users.profile', id=g.user['user_id']))
    #else:
    #    flash('Something went wrong')

    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/account/<string:id>')
@is_authenticated
def account(id):
    '''Controller for the user account'''

    image = url_for('static', filename="profile_img/default_avatar.png")
    return render_template('user_dashboard.html', image=image)

@users.route('/account/purchase_history/<string:id>')
def purchase_history(id):
    with db.connection.cursor() as cursor:
        db.reconnect()

        cursor.execute('CREATE VIEW purchase_history_user '
                       'AS SELECT p.name, oi.quantity, oi.total_price, pm.payment_name, s.store_name '
                       'FROM product p, order_item oi, payment_method pm, store s, transaction t '
                       'WHERE t.payment_method_id=pm.payment_method_id '
                       'AND t.store_id=s.store_id '
                       'AND t.order_item_id=oi.order_item_id '
                       'AND oi.product_id=p.product_id '
                       'AND t.user_id=(%s)',(id))

        db.connection.commit()

        cursor.execute('SELECT * FROM purchase_history_user')
        phu=cursor.fetchall()
        print(phu)


        cursor.execute('DROP VIEW purchase_history_user')

        db.connection.commit()

    return render_template('purchase_history_user.html', phu=phu)