from flask import render_template, redirect, url_for, Blueprint
from ecommerce.store.forms import StoreRegistrationForm
from ecommerce import mysql

store = Blueprint('store', __name__)

@store.route('/store')
def store_dashboard():
    return render_template("store_dashboard.html")

@store.route('/store/register', methods=['POST', 'GET'])
def store_register():
    form = StoreRegistrationForm()
    cursor = mysql.connect().cursor() 
    
    if form.validate_on_submit():
        # insert store object into store table
        cursor.execute('INSERT INTO store (name, about, address) VALUES (%s, %s, %s, %s)',
                (#(int(g.user['user_id']),
                form.name.data,
                form.about.data,
                form.address.data
                )) 

        # commit changes to db
        mysql.connect().commit()
        
        # close cursor
        cursor.close()
        
        print("Store commited to database")

        # redirect to store overview
        return redirect(url_for('store.store_dashboard'))

    return render_template('store_registration.html', form=form)

