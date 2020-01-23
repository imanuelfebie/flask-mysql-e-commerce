import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request

# Flask object
app = Flask(__name__) 

# Secret key
app.config['SECRET_KEY'] = '12345678' 

# Init sentry for flask
sentry_sdk.init(
    dsn="https://8b22654d815049f4b4097f30af22a07e@sentry.io/1883857",
    integrations=[FlaskIntegration()]
)

# routes import
from ecommerce.main.routes import main
from ecommerce.users.routes import users
from ecommerce.catalog.routes import catalog
from ecommerce.store.routes import store
from ecommerce.cart.routes import cart
from ecommerce.admin.routes import admin

app.register_blueprint(admin)
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(catalog)
app.register_blueprint(store)
app.register_blueprint(cart)
