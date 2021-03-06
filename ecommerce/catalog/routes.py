from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from ecommerce.catalog.forms import CategoryCreateForm, ProductCreateForm, ProductUpdateForm
from ecommerce.db import Database as db
#from ecommerce.users.routes import before_request as g
#from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

# Category list
@catalog.route('/categories')
def category_list():
    # retrieve all category object from database
    with db.connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(name) AS product_count, name AS p_name, category_name FROM product_view GROUP BY category_name')
        category_list = cursor.fetchall()

    return render_template('category_list.html', category_list=category_list)

# Add product
@catalog.route('/store/<string:id>/products/new', methods=['GET', 'POST'])
def product_create(id):
    form = ProductCreateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect by default because heroku server connection is unstable
        db.reconnect()
        
        # get this store_id
        #cursor.execute('SELECT * FROM user WHERE store_id=(%s)', (id))
        #user = cursor.fetchone()

        # select all categories
        cursor.execute('SELECT * FROM category')
        category_list = cursor.fetchall()
        form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]

        if form.validate_on_submit():
            cursor.execute('''INSERT INTO product (name, price, available, category_id, description, store_id) VALUES (%s, %s, %s, %s, %s, %s)''', (
                                  form.name.data,
                                  form.price.data,
                                  True,
                                  form.category.data,
                                  form.description.data,
                                  g.user['store_id']))
            # Commit changes to db
            db.connection.commit()
            flash('Product added')
        
            return redirect(url_for('store.store_manager', id=g.user['store_id']))
 
    return render_template('product_create.html', form=form)

# Product details
@catalog.route('/product/<string:id>')
def product_detail(id):
    '''Retrieve one product by id'''
    
    with db.connection.cursor() as cursor:
        db.reconnect()
        # Retrieve product details with related data from category and store table
        cursor.execute('SELECT * FROM product p '
                       'INNER JOIN category c ON p.category_id=c.category_id ' 
                       'INNER JOIN store s ON p.store_id=s.store_id ' 
                       'WHERE p.product_id=(%s)', (id))
        product = cursor.fetchone()
        
        # retrieve products from this product's store
        #cursor.execute('SELECT p.name, p.price FROM product p '
        #               'INNER JOIN store s ON p.store_id=s.store_id '
        #               'WHERE s.store_id=p.store_id')
        

    return render_template('product_detail.html', product=product)

@catalog.route('/product/update/<string:id>', methods=['GET','POST'])
def product_update(id):
    '''Controller to update produc object'''
    form = ProductUpdateForm()
    
    with db.connection.cursor() as cursor:
        # reconnect to heroku cleardb database
        db.reconnect()
        # get this product
        cursor.execute('SELECT * FROM product WHERE product.product_id=(%s)', (id))
        product = cursor.fetchone()
        
        # Get the categories
        cursor.execute('SELECT * FROM category')
        category_list = cursor.fetchall()
        form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]

        # populate fields with current data
        form.name.data = product['name']
        form.price.data = product['price']    
        form.category.data = product['category_id']
        form.description.data = product['description']

        if form.validate_on_submit():
            # insert the updated data into product
            cursor.execute('UPDATE product '
                       'SET name=(%s), price=(%s), category_id=(%s), description=(%s) '
                       'WHERE product_id=(%s)', (
                        request.form['name'],
                        request.form['price'],
                        request.form['category'],
                        request.form['description'],
                        id))
            # commit updates
            db.connection.commit()
            
            flash('{} has been updated'.format(product['name']))
            
            return redirect(url_for('store.store_manager', id=g.user['store_id']))
        else:
            # show error if something went wrong
            flash('Something went wrong. {}'.format(form.errors))

    return render_template('product_update.html', form=form, product=product)

@catalog.route('/product/delete/<string:id>')
def product_delete(id):

    with db.connection.cursor() as cursor:
        # reconnect to heroku clear_db
        db.reconnect()
        # delete product from database
        cursor.execute('DELETE FROM product WHERE product.product_id=%s', (int(id)))
        db.connection.commit()
        
        # success message
        flash('Product deleted')

        return redirect(url_for('store.store_manager', id=g.user['store_id']))
        





