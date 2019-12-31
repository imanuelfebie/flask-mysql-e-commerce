from flask import render_template
from ecommerce import app

@app.route('/')
def index():
    return render_template('index.html')
