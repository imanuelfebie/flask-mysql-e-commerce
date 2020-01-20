from flask import render_template, redirect, url_for, Blueprint, g, session
from ecommerce.store.forms import StoreRegistrationForm
from ecommerce.db import Database as db

store = Blueprint('store', __name__)

@store.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@store.route('/store/<string:id>')
def store_dashboard(id):
    with db.connection.cursor() as cursor:
        db.reconnect()
        cursor.execute("SELECT * FROM user,store WHERE (%s)=store.store_id", (g.user['store_id']))
        object = cursor.fetchone()

    return render_template("store_dashboard.html", object=object)

@store.route('/store/register/<string:id>', methods=['POST', 'GET'])
def store_register(id):
    form = StoreRegistrationForm()
    
    if form.validate_on_submit():
       # # insert store object into store table
       # cursor.execute('INSERT INTO store (name, about, address) VALUES (%s, %s, %s, %s)',
       #         (#(int(g.user['user_id']),
       #         form.name.data,
       #         form.about.data,
       #         form.address.data
       #         )) 

       # # commit changes to db
       # mysql.connect().commit()
       # 
       # # close cursor
       # cursor.close()
        
        print("Store commited to database")

        # redirect to store overview
        return redirect(url_for('store.store_dashboard'))

    return render_template('store_registration.html', form=form)

