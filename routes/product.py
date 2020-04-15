from flask import Blueprint, request, jsonify
from models import db, Product
from flask_jwt_extended import (
    jwt_required
)
route_products = Blueprint('route_products', __name__)
@route_products.route('/products', methods=['GET','POST'])
@route_products.route('/products/<int:id>', methods=['GET','PUT','DELETE'])
@route_products.route('/products/category/<int:category_id>', methods=['GET', 'POST'])
@route_products.route('/products/category/<int:category_id>/product/<int:id>', methods=['GET', 'POST'])
@jwt_required
def products(id=None, category_id =None):
    if request.method == 'GET':
        if id is not None and category_id is not None:
            product = Product.query.filter_by(category_id=category_id, id = id).first()
            if product:
                return jsonify(product.serialize()), 200
            else:
                return jsonify({"product":"Not found"}), 404
        elif id is not None:
            product = Product.query.get(id)
            if product:
                return jsonify(product.serialize()), 200
            else:
                return jsonify({"product": "Not found"})
        elif category_id is not None:
            products = Product.query.filter_by(category_id=category_id).all()
            products = list(map(lambda product: product.serialize(),products))
            return jsonify(products), 200
        else:
            products = Product.query.all()
            products = list(map(lambda product: product.serialize(),products))
            return jsonify(products), 200
    
    if request.method == 'POST':
        thing_name = request.json.get('thing_name')
        price = request.json.get('price')
        description = request.json.get('description')
        not_available = request.json.get('not_available')
        category_id = request.json.get('category_id')
        if not thing_name:
            return jsonify({"msg": "Name is required"}), 422 
        if not price:
            return jsonify({"msg": "price is required"}), 422 
        if not description:
            return jsonify({"msg": "description is required"}), 422
        if not not_available:
            return jsonify({"msg": "product is not available"}), 422
        if not category_id:
            return jsonify({"msg": "category_id is not available"}), 422
        
        product = Product()
        product.thing_name = thing_name
        product.price = price
        product.description = description
        product.not_available = not_available
        product.category_id = category_id
        db.session.add(product)
        db.session.commit()
        return jsonify(product.serialize()), 201
    
    if request.method == 'PUT':
        
        product = Product.query.get(id)
        product.thing_name = request.json.get('thing_name')
        product.price = request.json.get('price')
        product.description = request.json.get('description')
        product.not_available = request.json.get('not_available')
        product.quantity = request.json.get('quantity')
        db.session.commit()
        return jsonify(product.serialize()), 200
    if request.method == 'DELETE':
        
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'product':'Deleted'}), 200


