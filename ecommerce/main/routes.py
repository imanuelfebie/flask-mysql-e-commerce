from flask import Blueprint, render_template, session, g
from ecommerce import mysql

main = Blueprint('main', __name__)

@main.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

@main.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@main.route('/')
def index():
    # retrieve all product objects from the databse
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM product')
    product_list = cursor.fetchall()
    # close cursor
    cursor.close()

    return render_template('index.html', product_list=product_list)


