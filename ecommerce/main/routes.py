from flask import Blueprint, render_template
from ecommerce.catalog.models import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    product_list = Product.objects_all()

    return render_template('index.html', product_list=product_list)
