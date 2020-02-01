import pymysql
from flask import Blueprint, render_template, session, redirect, url_for, flash, g, request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from ecommerce.users.forms import (UserRegistrationForm, UserLoginForm, AddressCreateForm, 
                                   ProfileUpdateForm, AddressUpdateForm, UserPasswordUpdateForm)
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
    session.pop('user', None)
    session.pop('is_authenticated', False)
    return redirect(url_for('users.user_login'))


@users.route('/register', methods=['POST', 'GET'])
def register():
    '''Controller for registering new users'''
    form = UserRegistrationForm()
 
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            db.reconnect()
            # insert new user object into user
            cursor.execute('INSERT INTO user (firstname, lastname, email, password, is_active) VALUES (%s, %s, %s, %s, %s)', (
            form.firstname.data,
            form.lastname.data,
            form.email.data,
            generate_password_hash(form.password1.data),
            True))

            # commit to db
            db.connection.commit()

            # select new registered user
            cursor.execute('SELECT user_id FROM user WHERE email LIKE (%s)', (
                            form.email.data))
            user = cursor.fetchone() 
            session.pop('user', None)
            
            session['is_authenticated'] = True
            session['user'] = user
        
        flash('Awesome! You just created an account and can now login')
        
        # redirect user to address form
        return redirect(url_for('users.register_address', id=user['user_id']))

    else:
        print(form.errors)
        print('Failed to insert new user to db')

    return render_template('register.html', form=form)

@users.route('/register/address/<string:id>', methods=['GET', 'POST'])
@is_authenticated
def register_address(id):
    form = AddressCreateForm()
    
    with db.connection.cursor() as cursor:
        db.reconnect()

        # select cities
        cursor.execute('SELECT * FROM city')
        city_list = cursor.fetchall()
        form.city.choices = [(city['city_id'], city['name']) for city in city_list]

        if form.validate_on_submit():
            cursor.execute("INSERT INTO address (line1, line2, line3, postal_code, city_id) VALUES (%s, %s, %s, %s, %s)", (
                            form.line1.data,
                            form.line2.data,
                            form.line3.data,
                            form.postal_code.data,
                            form.city.data))
            # save address
            db.connection.commit()

            # select address
            cursor.execute("SELECT address_id FROM address WHERE line1=%s", (
                            form.line1.data))
            address = cursor.fetchone()
            
            # insert address
            cursor.execute("UPDATE user SET address_id = %s WHERE user_id = %s", (
                            address['address_id'],
                            id))
            db.connection.commit()

            flash('User has been created. Sign in with your email and password')
            
            return redirect(url_for('users.logout'))
    if form.errors:
        print(form.errors)

    return render_template('register_address.html', form=form)

@users.route('/profile/<string:id>', methods=['GET', 'POST'])
@is_authenticated
def profile(id):
    '''render the user profile details'''
    password_form = UserPasswordUpdateForm()
    address_form =AddressUpdateForm()
    profile_form = ProfileUpdateForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku mysql db
        db.reconnect()
        
        # get all cities for select form
        cursor.execute('''SELECT city_id, name FROM city''')
        city_list = cursor.fetchall()
        address_form.city.choices = [(city['city_id'], city['name']) for city in city_list]

        # get data from current user
        cursor.execute('SELECT firstname, lastname, email, address_line1, address_line2, address_line3, postal_code, city_id, city_name FROM customer_view WHERE user_id=%s',(
                        id))
        user = cursor.fetchone()

    # Populate user detail fields
    profile_form.email.data = user['email']
    profile_form.firstname.data = user['firstname']
    profile_form.lastname.data = user['lastname']

    address_form.address_line1.data = user['address_line1']
    address_form.address_line2.data = user['address_line2']
    address_form.address_line3.data = user['address_line3']
    address_form.postal_code.data = user['postal_code']
    address_form.city.data = user['city_id'] 

    return render_template('profile.html',user=user, profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/profile/update/<string:id>', methods=['GET','POST'])
@is_authenticated
def profile_update(id):
    '''Controller to update the user's email, name, lastname'''

    profile_form = ProfileUpdateForm()
    address_form = AddressUpdateForm()
    password_form = UserPasswordUpdateForm()
   
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()

        if profile_form.validate_on_submit():
            cursor.execute('UPDATE customer_view SET firstname=%s, lastname=%s, email=%s WHERE user_id=%s', (
                            request.form['firstname'],
                            request.form['lastname'],
                            request.form['email'],
                            id)) 
            db.connection.commit()
             
            flash('Successfully updated')

            return redirect(url_for('users.profile', id=g.user['user_id']))
       
    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/profile/update/password/<string:id>', methods=['POST', 'GET'])
@is_authenticated
def password_update(id):
    '''Controller to handle the password update form'''

    #profile_form = UserUpdateForm()
    #address_form = AddressUpdateForm()
    profile_form = ProfileUpdateForm()
    address_form = AddressUpdateForm()
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

    profile_form = ProfileUpdateForm()
    address_form = AddressUpdateForm()
    password_form = UserPasswordUpdateForm()

    with db.connection.cursor() as cursor:
        # reconnect to heroku mysql db
        db.reconnect()
        
        # get all cities for select form
        cursor.execute('''SELECT city_id, name FROM city''')
        city_list = cursor.fetchall()
        address_form.city.choices = [(city['city_id'], city['name']) for city in city_list]


        if address_form.validate_on_submit():
            # Update the address from current user using the customer_view
            cursor.execute('UPDATE customer_view SET address_line1=%s, address_line2=%s, address_line3=%s, postal_code=%s, city_id=%s WHERE user_id=%s', (
                            request.form['address_line1'],
                            request.form['address_line2'],
                            request.form['address_line3'],
                            request.form['postal_code'],
                            request.form['city'],
                            id))
            # commit update
            cursor.connection.commit()
                       
            flash('Successfully updated address')

            return redirect(url_for('users.profile', id=g.user['user_id']))
    print(request.form.errors)

    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/account/<string:id>')
@is_authenticated
def account(id):
    '''Controller for the user account'''

    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        cursor.execute('SELECT firstname, lastname, email, address_line1, address_line2, address_line3, postal_code, city_id, city_name FROM customer_view WHERE user_id=%s',(
                id))
        user = cursor.fetchone()

    image = url_for('static', filename="profile_img/default_avatar.png")

    return render_template('user_dashboard.html', image=image, user=user)

@users.route('/account/purchase_history/<string:id>')
def purchase_history(id):

    with db.connection.cursor() as cursor:
        db.reconnect()
        # SELECT ALL transaction from this user
        cursor.execute('SELECT t.transaction_id, t.ordered_on FROM transaction t WHERE t.user_id=%s', (id))
        transaction_list = cursor.fetchall()
        cursor.execute('SELECT firstname, lastname, email, address_line1, address_line2, address_line3, postal_code, city_id, city_name FROM customer_view WHERE user_id=%s',(
                    id))
        user = cursor.fetchone()

    return render_template('purchase_history_user.html', transaction_list=transaction_list, user=user)
       
