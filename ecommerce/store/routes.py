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
def store_detail(id):
    '''Display the store\'s name & owner'''

    with db.connection.cursor() as cursor:
        db.reconnect()
        # Inner join to get the the necessary data to display
        # the
        cursor.execute('''SELECT u.firstname, u.lastname, s.name
                          FROM user u
                          INNER JOIN store s
                          ON u.store_id=s.store_id
                          WHERE s.store_id = (%s)
                          ''', (id))
        # fetch the data
        object = cursor.fetchone()
    
    return render_template("store_detail.html", object=object)

@store.route('/store/manager/<string:id>')
def store_manager(id):
    return render_template('store_manager.html')

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

