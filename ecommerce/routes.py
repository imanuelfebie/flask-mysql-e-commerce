from flask import render_template, redirect, url_for, request
from .forms import UserRegistrationForm, StoreRegistrationForm
from ecommerce import app



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register_user():
    form = UserRegistrationForm() # instance of the UserRegistrationForm
    
    # if form.validate_on_submit():

    return render_template('register.html', form=form)
