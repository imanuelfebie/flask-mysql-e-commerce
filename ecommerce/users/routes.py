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
                return redirect(url_for('users.user_dashboard', id=user['user_id']))

            # display if any errors occur
            flash(error)

    return render_template('login.html', form=form)
    
@users.route('/logout')
@is_authenticated
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@users.route('/register', methods=['POST', 'GET'])
def register():
    form = UserRegistrationForm()

    
    if form.validate_on_submit():
        # insert new user object into user
        with db.connection.cursor() as cursor:
            try:
                cursor.execute('INSERT INTO user (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)', (
                    form.firstname.data,
                    form.lastname.data,
                    form.email.data,
                    generate_password_hash(form.password1.data)
                    ))
                # commit to db
                db.connection.commit()
            except (pymysql.OperationalError):
                cursor.execute('INSERT INTO user (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)', (
                    form.firstname.data,
                    form.lastname.data,
                    form.email.data,
                    generate_password_hash(form.password1.data)
                    ))
                # commit to db
                db.connection.commit()

        flash('Awesome! You just created an account and can now login')
        
        # redirect user to address form
        return redirect(url_for('users.register_address', id=g.user['user_id']))

    else:
        print(form.errors)
        print('Failed to insert new user to db')

    return render_template('register.html', form=form)

@users.route('/register/address/', methods=['GET','POST'])
def register_address():
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
    db.reconnect()
    # render the forms
    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()

    # Populate user detail fields
    profile_form.email.data = g.user['email']
    profile_form.firstname.data = g.user['firstname']
    profile_form.lastname.data = g.user['lastname']
    
    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/profile/update/<string:id>', methods=['GET','POST'])
@is_authenticated
def profile_update(id):
    '''Handles updating the user details - email, firstname & lastname'''
    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()
    
    # Populate user detail fields
    #profile_form.email.data = g.user['email']
    #profile_form.firstname.data = g.user['firstname']
    #profile_form.lastname.data = g.user['lastname']
    #print(g.user['email'])

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


@users.route('/profile/update/address', methods=['POST', 'GET'])
@is_authenticated
def address_update():
    profile_form = UserUpdateForm()
    address_form = AddressCreateForm()
    password_form = UserPasswordUpdateForm()
    
    return render_template('profile.html', profile_form=profile_form, address_form=address_form, password_form=password_form)

@users.route('/dashboard/<string:id>')
@is_authenticated
def user_dashboard(id):
    '''User account dashboard'''
    return render_template('user_dashboard.html')
