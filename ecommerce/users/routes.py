from flask import Blueprint, render_template
from .forms import UserRegistrationForm
from ecommerce import mysql

users = Blueprint('users', __name__)

@users.route('/register')
def register():
    form = UserRegistrationForm()
    
    return render_template('register.html', form=form)

@users.route('/login')
def login():
	form = UserRegistrationForm()

	return render_template('login.html', form=form)