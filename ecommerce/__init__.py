from flask import Flask, request
from ecommerce.db import Database
from flask_login import LoginManager

# Flask object
app = Flask(__name__) 

# Secret key
app.config['SECRET_KEY'] = '12345678' 

# Database object
mysql = Database()

login_manager = LoginManager(app)

# routes import
from ecommerce.main.routes import main
from ecommerce.users.routes import users
from ecommerce.catalog.routes import catalog
from ecommerce.store.routes import store

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(catalog)
app.register_blueprint(store)
