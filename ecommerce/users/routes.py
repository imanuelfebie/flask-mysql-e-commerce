from flask import Blueprint, render_template, session, redirect, url_for, flash, g
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import UserRegistrationForm, AdminLogin, StoreRegistrationForm, UserLoginForm
from ecommerce.users.models import User, Store
#from ecommerce import mysql, login_manager
from ecommerce.catalog.models import Basket,Total

users = Blueprint('users', __name__)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

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
        '''User login'''
        form = UserLoginForm()
        error = None

        if form.validate_on_submit():
            user = User.filter_by(form.email.data)
            session.pop('user', None)
            if user is None:
                error = 'User doesn\'t exist'
            elif not check_password_hash(user['password'], form.password.data):
                error = 'Please insert correct username and password'
            else:
                #login_user(user)
                # print(session['user'])
                session['user'] = user
                #user['is_authenticated'] = True
                return redirect(url_for('users.user_dashboard'))

            flash(error)

        return render_template('login.html', form=form)
    else:
        return redirect(url_for('users.user_dashboard'))


#session.pop('user', None)

@users.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))


@users.route('/register', methods=['POST', 'GET'])
def register():
    '''User registration page'''
    form = UserRegistrationForm()
    message = None

    if form.validate_on_submit():
        user = User(
                form.email.data,
                form.firstname.data,
                form.lastname.data,
                generate_password_hash(form.password1.data)
                )
        user.create_object()   
        flash('Awesome! You just created an account and can now login')
        return redirect(url_for('users.user_login'))

    return render_template('register.html', form=form)

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

@users.route('/store-register', methods=['POST', 'GET'])
def storeRegister():
    form = StoreRegistrationForm()

    if form.validate_on_submit():
        store = Store(
                form.name.data,
                form.about.data,
                form.address.data,
                )
        store.create_object()

        print('Success')
    
    return render_template('store_registration.html', form=form)

@users.route('/store-dashoard')
def store_dashboard():
    return render_template('store_dashboard.html')

