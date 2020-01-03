from flask import Flask
from flask_mysqldb import MySQL
import yaml

# Flask object
app = Flask(__name__) 

# Secret key
app.config['SECRET_KEY'] = '12345678'

# Database config
db_config = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['username']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']

db = MySQL(app) # MySQL instance and passing the Flask object as an argument

from ecommerce import routes
