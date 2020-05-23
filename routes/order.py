from flask import Blueprint, request, jsonify
from models import db, Order
from flask_jwt_extended import (
    jwt_required
)
route_orders = Blueprint('route_orders', __name__)
@route_orders.route('/orders', methods=['GET','POST'])
@route_orders.route('/orders/procent/<int:procent>', methods=['GET','POST'])
@route_orders.route('/orders/<int:id>', methods=['GET','PUT','DELETE'])
@route_orders.route('/orders/negocio/<int:negocio_id>', methods=['GET'])
@route_orders.route('/orders/procent/<int:procent>/negocio/<int:negocio_id>', methods=['GET','POST'])
@jwt_required
def orders(id=None, negocio_id = None, procent = None):
    if request.method == 'GET':
        if id is not None:
            order = Order.query.get(id)
            if order:
               return jsonify(order.serialize()), 200
            else:
                return jsonify({"order": "Not Found"})
        elif negocio_id is not None:
            orders = Order.query.filter_by(negocio_id=negocio_id).all()
            orders = list(map(lambda order: order.serialize(), orders))
            return jsonify(orders), 200
        elif procent is not None:
            orders = Order.query.filter_by(procent=procent).all()
            orders = list(map(lambda order: order.serialize(), orders))
            return jsonify(orders), 200
        elif negocio_id is not None and procent is not None:
            orders = Order.query.filter_by(negocio_id=negocio_id).all()
            orders = list(map(lambda order: order.serialize(), orders))
            orders = Order.query.filter_by(procent=procent).all()
            orders = list(map(lambda order: order.serialize(), orders))
            return jsonify(orders), 200
        else:
            orders = Order.query.all()
            orders = list(map(lambda order: order.serialize(),orders))
            return jsonify(orders), 200
    
    if request.method == 'POST':
        price = request.json.get('price')
        consumer_id = request.json.get('consumer_id')
        product_details = request.json.get('product_details')
        negocio_id = request.json.get('negocio_id')
        comment = request.json.get('comment')
        times = request.json.get('times')
        if not price:
            return jsonify({"msg": "Price is required"}), 422 
        if not consumer_id:
            return jsonify({"msg": "consumer_id is required"}), 422 
        if not product_details:
            return jsonify({"msg": "product_details is required"}), 422
        if not negocio_id:
            return jsonify({"msg": "negocio_id is required"}), 422 
        order = Order()
        order.price = price
        order.consumer_id = consumer_id
        order.product_details = product_details
        order.negocio_id = negocio_id
        order.comment = comment
        order.times = times
        db.session.add(order)
        db.session.commit()
        return jsonify(order.serialize()), 201
    
    if request.method == 'PUT':
        
        order = Order.query.get(id)
        order.procent = request.json.get('procent')
        db.session.commit()
        return jsonify(order.serialize()), 200
    if request.method == 'DELETE':
        
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'order':'Deleted'}), 200