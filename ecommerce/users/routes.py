from flask import Blueprint, render_template
from .forms import UserRegistrationForm

users = Blueprint('users', __name__)

@users.route('/')
def register():
    form = UserRegistrationForm()
    
    return render_template('register.html', form=form)
