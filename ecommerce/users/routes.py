from flask import Blueprint, render_template
from .forms import UserRegistrationForm, AdminLogin
from ecommerce.users.models import User
from ecommerce import mysql, login_manager
from ecommerce.catalog.models import Basket

users = Blueprint('users', __name__)

#def load_user(user_id):


@users.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLogin()

    return render_template('admin_login.html', form=form)

@users.route('/register', methods=['POST', 'GET'])
def register():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        user = User(
                form.email.data,
                form.firstname.data,
                form.lastname.data,
                form.password1.data
                )
        user.create_object()

        print('Success')
        print(form.firstname.data)
        print(form.lastname.data)
        print(form.email.data)
        print(form.password1.data)
        print(form.password2.data)
    
    return render_template('register.html', form=form)

@users.route('/login')
def login():
	form = UserRegistrationForm()

	return render_template('login.html', form=form)

@users.route('/basket_list')
def basket_list():
    basket_list = Basket.objects_all()
    total_price= Basket.total_price()

    return render_template('index.html', basket_list=basket_list, total_price=total_price)
