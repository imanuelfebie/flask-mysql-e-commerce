from flask import Blueprint, render_template, redirect, url_for, request, flash
from ecommerce.catalog.forms import CategoryCreateForm
from ecommerce.catalog.models import Category, Product
from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.route('/add-category', methods=['GET', 'POST'])
def category_create():
    form = CategoryCreateForm()
    
    if request.method == 'POST':
        category = Category(name=form.name.data)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO category (name) VALUES (%s)", (category.name))
        mysql.connection.commit()

        return 'Success'
    else:
        # print this if commit to database fails
        print('Commit failed')

    return render_template('catagory_create.html', form=form)

@catalog.route('/products')
def product_list():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM product''')
    product_list = cur.fetchall()
    
    return render_template('product_list.html', product_list=product_list)


