from flask import Blueprint, render_template, session, redirect, url_for, flash, g
#from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from ecommerce.users.forms import UserRegistrationForm, AdminLogin, StoreRegistrationForm, UserLoginForm, AddressCreateForm
from ecommerce.users.models import User, Store
#from ecommerce import mysql, login_manager
from ecommerce import mysql
from ecommerce.catalog.models import Basket,Total,Payment

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

    if not g.user:
        form = UserLoginForm()
        error = None

        if form.validate_on_submit():
            # retrieve user from the database where the email equals the input value
            mysql.reconnect()
            mysql.cursor.execute('SELECT * FROM user WHERE email LIKE (%s)', (form.email.data))
            user = mysql.cursor.fetchone() 
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

    if form.validate_on_submit():
        # insert new user object into user
        mysql.reconnect()
        mysql.cursor.execute('INSERT INTO user (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)', (
            form.firstname.data,
            form.lastname.data,
            form.email.data,
            generate_password_hash(form.password1.data)
            ))

        # commit to db
        mysql.connect.commit()

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
    

@users.route('/basket_list')
def basket_list():
    basket_list = Basket.objects_all()
    total_price= Total.total_price()

    return render_template('basket_list.html', basket_list=basket_list, total_price=total_price)

@users.route('/payment')
def payment():
    payment=Payment.payment_method()

    return render_template('payment.html', payment=payment)

@users.route('/store/register', methods=['POST', 'GET'])
def storeRegister():
    form = StoreRegistrationForm()
    print(g.user['user_id']) 
    # retrieve user
    # mysql.reconnect()
    # mysql.cursor.execute('select * from user, store where user.id = store.id')
    # user = mysql.cursor.fetchone()
    
    if form.validate_on_submit():
        # insert store object into store table
        mysql.reconnect()
        mysql.cursor.execute('INSERT INTO store (user_id, name, about, address) VALUES (%s, %s, %s, %s)',
                (int(g.user['user_id']),
                form.name.data,
                form.about.data,
                form.address.data
                ))

        print(g.user['user_id'])
        print(form.errors)
        # commit changes to db
        mysql.connect.commit()

        # redirect to store overview
        return redirect(url_for('users.store_dashboard'))

    return render_template('store_registration.html', form=form)

@users.route('/store-dashboard')
def store_dashboard():
    print(g.user)
    return render_template('store_dashboard.html')

