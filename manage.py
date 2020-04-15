#import stripe
#import json
import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import(
    JWTManager
)
#from dotenv import load_dotenv, find_dotenv

from models import Consumer, db, Driver, Product, Category, Order, ConsumerBusiness, Negocio#, Current_order, Business_day, Promocode, Bank_info, Card, Payment_method, History_order, Rating_driver, Rating_business
from routes.consumer import route_consumers
from routes.authconsumer import authconsumer
from routes.driver import route_drivers
from routes.category import route_categories
from routes.product import route_products
from routes.authdriver import authdriver
from routes.order import route_orders
from routes.getallbusiness import route_businessesall
from routes.noauthcategories import route_categoriesnoauth
from routes.facebook import authfbconsumer
from routes.consumerbusiness import route_consumerbusinesses
from routes.authconsumerbusiness import authconsumerbusiness
from routes.negocio import route_negocios
from routes.noauthproduct import route_noauthproducts
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secrets'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1000)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', name = 'home')

app.register_blueprint(authconsumer)
app.register_blueprint(route_consumers)
app.register_blueprint(route_drivers)
app.register_blueprint(authdriver)
app.register_blueprint(route_categories)
app.register_blueprint(route_products)
app.register_blueprint(route_orders)
app.register_blueprint(route_businessesall)
app.register_blueprint(route_categoriesnoauth)
app.register_blueprint(authfbconsumer)
app.register_blueprint(authconsumerbusiness)
app.register_blueprint(route_consumerbusinesses)
app.register_blueprint(route_negocios)
app.register_blueprint(route_noauthproducts)
app.register_blueprint(route_categoriesnoauth)

if __name__ == '__main__':
    manager.run()