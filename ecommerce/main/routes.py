import pymysql

from flask import Blueprint, render_template, session, g
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
        try: 
            cursor.execute("SELECT * FROM product")
            product_list = cursor.fetchall()
        except (pymysql.OperationalError):
            db.reconnect()
            cursor.execute("SELECT * FROM product")
            product_list = cursor.fetchall()
    
    return render_template('index.html', product_list=product_list)


