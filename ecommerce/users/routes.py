from flask import Blueprint, render_template
from .forms import UserRegistrationForm
from ecommerce import mysql

users = Blueprint('users', __name__)

@users.route('/register')
def register():
    form = UserRegistrationForm()
    
    return render_template('register.html', form=form)

@users.route('/users')
def user_list():
    c = mysql.connection.cursor()
    c.execute('''SELECT * FROM user''')
    users = c.fetchall()

    return render_template('users.html', users=users)
