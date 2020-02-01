from flask import Blueprint, render_template, session, g, url_for, redirect
from ecommerce.db import Database as db

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@main.route('/')
def index():
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()
        
        # get categories
        cursor.execute('SELECT DISTINCT * FROM category LIMIT 10')
        category_list = cursor.fetchall() 
         
        # get products
        cursor.execute("SELECT * FROM product_view")
        product_list = cursor.fetchall()
 
    return render_template('index.html', product_list=product_list, category_list=category_list)

@main.route('/category/<string:name>')
def filtered_by_category(name):
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku
        db.reconnect()

        cursor.execute('SELECT DISTINCT * FROM category')
        category_list = cursor.fetchall()
        
        cursor.execute('SELECT * FROM product_view WHERE category_name LIKE (%s)', (
                        name))
        product_list = cursor.fetchall()
        
    return render_template('product_filtered_by_category.html', product_list=product_list, category_list=category_list)


