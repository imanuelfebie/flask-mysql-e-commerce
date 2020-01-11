from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from ecommerce.catalog.forms import CategoryCreateForm, ProductCreateForm
#from ecommerce.users.routes import before_request as g
from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@catalog.route('/add-category', methods=['GET', 'POST'])
def category_create():
    form = CategoryCreateForm()
    
    if form.validate_on_submit():
        # create cursor and insert form data into category table
        cursor = mysql.connect().cursor() 
        cursor.execute('INSERT INTO category (name) VALUES (%s)',
                (form.name.data))

        # commit changes to database
        mysql.connect().commit() 

        # close cursor
        cursor.close()

    else:
        # print this if commit to database fails
        print(request.args.get('name'))
        print('Commit failed')

    return render_template('catagory_create.html', form=form)

@catalog.route('/categories')
def category_list():
    # retrieve all category object from database
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM category')
    category_list = cursor.fetchall()
    
    # close the cursor
    cursor.close()

    return render_template('category_list.html', category_list=category_list)

@catalog.route('/add-product', methods=['GET', 'POST'])
def product_create():
    form = ProductCreateForm()

    # retrieve all categories from db
    cursor = mysql.connect().cursor()
    category_list = cursor.execute("SELECT * FROM category")

    if g.user:            
        if form.validate_on_submit():
            # Insert form data into db
            cursor.execute('''
                    INSERT INTO product (name, description, stock, price, available, category, store_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        form.name.data,
                        form.description.data,
                        form.stock.data,
                        form.price.data,
                        form.available.data,
                        form.category.data,
                        form.store_id.data)) 

            # commit changes to database
            mysql.connect().commit()
            print("Product added")
            # redirect user to his product overview page
        else:
            print("Adding product failed")

        return render_template('product_create.html', form=form, category_list=category_list)
