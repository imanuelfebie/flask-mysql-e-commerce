from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from ecommerce.catalog.forms import CategoryCreateForm, ProductCreateForm
from ecommerce.db import Database as db
#from ecommerce.users.routes import before_request as g
#from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@catalog.route('/categories/new', methods=['GET', 'POST'])
def category_create():
    '''Adding new categories, this page should only be accessible for the admin'''
    form = CategoryCreateForm()
    
   # if form.validate_on_submit():
   #     # create cursor and insert form data into category table
   #     cursor = db.connection().cursor() 
   #     cursor.execute('INSERT INTO category (name) VALUES (%s)', (form.name.data))

   #     # commit changes to database
   #     db.connection().commit() 
   #     cursor.close()

   #     return redirect(url_for('catalog.category_list'))

   # else:
   #     # print this if commit to database fails
   #     print(request.args.get('name'))
   #     print(form.errors)
   #     print('Commit failed')

    return render_template('catagory_create.html', form=form)

# Category list
@catalog.route('/categories')
def category_list():
    # retrieve all category object from database
    with db.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM category')
        category_list = cursor.fetchall()

    return render_template('category_list.html', category_list=category_list)

# Add product
@catalog.route('/store/<string:id>/products/new', methods=['GET', 'POST'])
def product_create(id):
    form = ProductCreateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect by default because heroku server connection is unstable
        db.reconnect()
        cursor.execute('SELECT * FROM category')
        category_list = cursor.fetchall()
        form.category.choices = [(category['category_id'], category['name']) for category in category_list]

        if form.validate_on_submit():
            cursor.execute('''INSERT INTO product 
                              (name, price, available, category_id, store_id) VALUES (%s, %s, %s, %s, %s)''', (
                                  form.name.data,
                                  form.price.data,
                                  int(1),
                                  form.category.data,
                                  form.store_id.data
                                  ))
            # Commit changes to db
            db.connection.commit()
            flash('Product added')
            return redirect(url_for('store.store_manager', id=g.user['store_id']))

        else:
            print('fail')
            print(form.category.data)
            print(form.errors)
     
    return render_template('product_create.html', form=form)

# Product details
@catalog.route('/product/<string:id>')
def product_detail(id):
    '''Retrieve one product by id'''
    
    with db.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM product WHERE product_id = (%s)', id)
        product = cursor.fetchone()

    return render_template('product_detail.html', product=product)
