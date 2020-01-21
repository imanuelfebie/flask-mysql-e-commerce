from flask import Blueprint, render_template, redirect, url_for, session, g
from ecommerce.cart.cart import Cart

cart = Blueprint('cart', __name__)

@cart.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@cart.route('/cart')
def shopping_cart():
    return render_template('cart.html')
