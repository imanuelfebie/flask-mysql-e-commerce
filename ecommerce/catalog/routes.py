from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from ecommerce.catalog.forms import CategoryCreateForm, ProductCreateForm
from ecommerce.catalog.models import Category, Product
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
        category = Category(request.args.get('name'))
        category.create()
        return 'Object created'

    else:
        # print this if commit to database fails
        print(request.args.get('name'))
        print('Commit failed')

    return render_template('catagory_create.html', form=form)

@catalog.route('/categories')
def category_list():
    # retrieve all category object from database
    cursor = mysql.connect.cursor()
    cursor.execute('SELECT * FROM category')
    category_list = cursor.fetchall()
    # close the cursor
    cursor.close()

    return render_template('category_list.html', category_list=category_list)

@catalog.route('/products')
def product_list():
    # retrieve all product objects from database
    cursor = mysql.connect.cursor()
    cursor.execute('SELECT * FROM product')
    product_list = cursor.fetchall()
    # close the cursor
    cursor.close()
    
    return render_template('product_list.html', product_list=product_list)

@catalog.route('/add-product', methods=['GET', 'POST'])
def product_create():
    form = ProductCreateForm()
    category_list = Category.objects_all()

    if g.user:    
        if request.method == "POST":
            try:
                cvalue = request.form['cvalue']
            except:
                print("Select a category")


        if form.validate_on_submit():
            product = Product(
                form.name.data,
                form.description.data,
                form.stock.data,
                form.price.data,
                form.available.data,
                cvalue,
                form.store_id.data
                )
            product.create_object()

            print("Product added")
        else:
            print("Adding product failed")



        return render_template('product_create.html', form=form, category_list=category_list)



