from flask import Flask, request
from ecommerce.db import Database

#from flask_mysqldb import MySQL
#import yaml

# Flask object
app = Flask(__name__) 

# Secret key
app.config['SECRET_KEY'] = '12345678' 

mysql = Database()

# Database config
#db_config = yaml.load(open('local_db.yaml'))

#app.config['MYSQL_HOST'] = db_config['host']
#app.config['MYSQL_USER'] = db_config['username']
#app.config['MYSQL_PASSWORD'] = db_config['password']
#app.config['MYSQL_DB'] = db_config['database']


#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'batman'
#app.config['MYSQL_PASSWORD'] = 'password'
#app.config['MYSQL_DB'] = 'ecommerce_db'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL instance and passing the Flask object as an argument
#mysql = MySQL(app)

# routes import
from ecommerce.main.routes import main
from ecommerce.users.routes import users
from ecommerce.catalog.routes import catalog

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(catalog)
