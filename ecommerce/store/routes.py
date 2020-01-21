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
    
    '''NO CLUE YET ON HOW TO UPDATE THE CURRENT USER TO THIS STORE'''
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            # Insert form data into db
            cursor.execute('INSERT INTO store (name, about) VALUES (%s, %s)',
                   (form.name.data, form.about.data)) 
            # Commit changes to db
            db.connection.commit()

        #return redirect(url_for('store.store_dashboard'))

    return render_template('store_registration.html', form=form)

