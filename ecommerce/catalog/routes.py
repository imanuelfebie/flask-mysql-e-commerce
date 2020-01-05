from flask import Blueprint, render_template, redirect, url_for, request, flash
from ecommerce.catalog.forms import CategoryCreateForm
from ecommerce.catalog.models import Category, Product
from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.route('/add-category')
def category_create():
    form = CategoryCreateForm()
    
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        category.create()
        #flash(f'New category has been added')
        print('Category created')
        
        return redirect(url_for('main.index'))
    else:
        print('Commit failed')

    return render_template('catagory_create.html', form=form)

@catalog.route('/products')
def product_list():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM product''')
    product_list = cur.fetchall()
    
    return render_template('product_list.html', product_list=product_list)


