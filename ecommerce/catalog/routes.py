from flask import Blueprint, render_template, redirect, url_for, request, flash
from ecommerce.catalog.forms import CategoryCreateForm
from ecommerce.catalog.models import Category, Product
from ecommerce import mysql

catalog = Blueprint('catalog', __name__)

@catalog.route('/add-category', methods=['GET', 'POST'])
def category_create():
    form = CategoryCreateForm()
    
    if form.validate_on_submit():
        category = Category(form.name.data)
        category.create()
        return 'Object created'

    else:
        # print this if commit to database fails
        print(form.name.data)
        print('Commit failed')

    return render_template('catagory_create.html', form=form)

@catalog.route('/categories')
def category_list():
    category_list = Category.objects_all()
    return render_template('category_list.html', category_list=category_list)

@catalog.route('/products')
def product_list():
    product_list = Product.objects_all()

    return render_template('product_list.html', product_list=product_list)


