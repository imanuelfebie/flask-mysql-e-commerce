from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from ecommerce.users.forms import UserRegistrationForm, UserLoginForm, AddressCreateForm

from ecommerce import mysql

users = Blueprint('users', __name__)

@users.route('/getsession')
def get_session():
    if 'user' in session:
        return session['user']
    return 'Anynomous'

@users.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@users.route('/login', methods=['GET', 'POST'])
def user_login():
    cursor = mysql.connect().cursor()

    if not g.user:
        form = UserLoginForm()
        error = None

        if form.validate_on_submit():
            # retrieve user from the database where the email equals the input value
            cursor.execute('SELECT * FROM user WHERE email LIKE (%s)', (form.email.data))
            # fetch retreived user
            user = cursor.fetchone() 
            session.pop('user', None)

            if user is None:
                # checks if user exists, if not display error message
                error = 'User doesn\'t exist'
            
            elif not check_password_hash(user['password'], form.password.data):
                # checks if password matches when user exists, if not displays error message
                error = 'Please insert correct username and password'
            
            else:
                # start new session with user, redirect to dashboard page
                session['user'] = user
                cursor.close()
                return redirect(url_for('users.user_dashboard'))

            # display if any errors occur
            flash(error)

    return render_template('login.html', form=form)
    
@users.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))


@users.route('/register', methods=['POST', 'GET'])
def register():
    form = UserRegistrationForm()
    cursor = mysql.connect().cursor()

    if form.validate_on_submit():
        # insert new user object into user
        cursor.execute('INSERT INTO user (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)', (
            form.firstname.data,
            form.lastname.data,
            form.email.data,
            generate_password_hash(form.password1.data)
            ))

        # commit to db
        mysql.connect().commit()
        cursor.close()

        flash('Awesome! You just created an account and can now login')

        return redirect(url_for('users.user_login'))

    return render_template('register.html', form=form)

@users.route('/address-form', methods=['POST', 'GET'])
def update_address():
    form = AddressCreateForm()

    #if form.validate_on_submit():
     
    
    return redirect(url_for('users.update_address')) 
    

@users.route('/dashboard')
def user_dashboard():
    '''User account dashboard'''
    if not g.user:
        return redirect(url_for('users.user_login'))
    return render_template('user_dashboard.html')
    
#@users.route('/payment')
#def payment():
#    payment=Payment.payment_method()
#
#    return render_template('payment.html', payment=payment)
