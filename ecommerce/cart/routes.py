from flask import Blueprint, render_template, redirect, url_for
from ecommerce.cart.cart import Cart

cart = Blueprint('cart', __name__)

@cart.route('/cart')
def shopping_cart():
    return render_template('cart.html')
