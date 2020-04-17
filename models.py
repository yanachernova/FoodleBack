from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class Consumer(db.Model):
    __tablename__ = 'consumers'
    id = db.Column(db.Integer,primary_key = True)
    fullname = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = True)
    phone_number = db.Column(db.String(255), nullable = True)
    address = db.Column(db.PickleType, nullable = True)
    
    def __repr__(self):
        return 'Consumer %r' % self.fullname

    def serialize(self):
        return{
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
        }


class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = True)
    address = db.Column(db.String(255), nullable = True)
    phone_number = db.Column(db.String(255), nullable = True)

    def __repr__(self):
        return 'Driver %r' % self.fullname

    def serialize(self):
        return{
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'address': self.address,
            'phone_number': self.phone_number,
        }

class ConsumerBusiness(db.Model):
    __tablename__ = 'consumerbusinesses'
    id = db.Column(db.Integer,primary_key = True)
    fullname = db.Column(db.String(255), nullable = True)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = True)
    phone_number = db.Column(db.String(255), nullable = True)

    def __repr__(self):
        return 'ConsumerBusiness %r' % self.fullname

    def serialize(self):
        return{
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'phone_number': self.phone_number,
        }

class Negocio(db.Model):
    __tablename__ = 'negocios'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = True, default='')
    phone_number = db.Column(db.String(255), nullable = True, default='')
    address = db.Column(db.String(255), nullable = True, default='')
    delivery_price = db.Column(db.Integer, nullable = True , default='')
    consumerbusiness_id = db.Column(db.Integer, db.ForeignKey('consumerbusinesses.id'), nullable = True, default='')
    consumerbusiness = db.relationship(ConsumerBusiness, backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Negocio %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'phone_number':self.phone_number,
            'address':self.address,
            'delivery_price':self.delivery_price,
            'consumerbusiness': self.consumerbusiness.serialize() 
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = True)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable = False)
    negocio = db.relationship(Negocio, backref = backref('children', cascade = 'all, delete'))

    def __repr__(self):
        return 'Category %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'negocio': self.negocio.serialize() 
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    thing_name = db.Column(db.String(255), nullable = True)
    price = db.Column(db.Integer, nullable = True)
    description = db.Column(db.Text(), nullable = True)
    not_available = db.Column(db.Boolean, default = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = True)
    category = db.relationship(Category, backref = backref('children', cascade = 'all, delete'))
    quantity = db.Column(db.Integer, nullable = True, default = 1)
    
    def __repr__(self):
        return 'Product %r' % self.thing_name

    def serialize(self):
        return{
            'id': self.id,
            'thing_name': self.thing_name,
            'price': self.price,
            'description': self.description,
            'not_available': self.not_available,
            'category': self.category.serialize(),
            'quantity': self.quantity
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer,primary_key = True)
    price = db.Column(db.Integer, nullable = False)
    product_details = db.Column(db.PickleType, nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumers.id'), nullable = False)
    consumer = db.relationship(Consumer, backref = backref('children', cascade = 'all, delete'))
    driver = db.Column(db.PickleType, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    times = db.Column(db.String(255), nullable=True)
    procent = db.Column(db.Integer, nullable=True, default=0)
    negocio_id = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable = False)
    negocio = db.relationship(Negocio)

    def __repr__(self):
        return 'Order %r' % self.price

    def serialize(self):
        return{
            'id': self.id,
            'price': self.price,
            'product_details': self.product_details,
            'consumer': self.consumer.serialize(),
            'driver': self.driver,
            'comment': self.comment,
            'times': self.times,
            'procent': self.procent,
            'negocio': self.negocio.serialize(),
        }
