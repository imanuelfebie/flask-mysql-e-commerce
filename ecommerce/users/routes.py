from flask import Blueprint, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import UserRegistrationForm, AdminLogin, StoreRegistrationForm, UserLoginForm
from ecommerce.users.models import User, Store
from ecommerce import mysql, login_manager
from ecommerce.catalog.models import Basket,Total

users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@users.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    '''Admin login page'''
    form = AdminLogin()

    return render_template('admin_login.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def user_login():
    '''User login'''
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.filter_by(form.email.data)
        print(type(user))
        return redirect(url_for('users.user_dashboard'))

    return render_template('login.html', form=form)


@users.route('/register', methods=['POST', 'GET'])
def register():
    '''User registration page'''
    form = UserRegistrationForm()

    if form.validate_on_submit():
        user = User(
                form.email.data,
                form.firstname.data,
                form.lastname.data,
                generate_password_hash(form.password1.data, method='sha256')
                )
        user.create_object()   

        return redirect(url_for('users.user_login'))

    return render_template('register.html', form=form)

@users.route('/dashboard')
def user_dashboard():
    '''User account dashboard'''
    user = User.get(11)    

    return render_template('user_dashboard.html', user=user)

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
