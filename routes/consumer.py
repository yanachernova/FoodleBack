from flask import Blueprint, request, jsonify
from models import db, Consumer
from flask_bcrypt import Bcrypt
from flask_jwt_extended import(
    jwt_required
)
bcrypt = Bcrypt()
route_consumers = Blueprint('route_consumers', __name__)

@route_consumers.route('/consumers', methods = ['GET'])
@route_consumers.route('/consumers/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
@jwt_required
def consumers(id = None):
    if request.method == 'GET':
        if id is not None:
            consumer = Consumer.query.get(id)
            if consumer:
                return jsonify(consumer.serialize()), 200
            else:
                return jsonify({"consumer": "Not found"}), 404
        else:
            consumers = Consumer.query.all()
            consumers = list(map(lambda consumer: consumer.serialize(), consumers))
            return jsonify(consumers), 200

    if request.method == 'PUT':
        consumer = Consumer.query.get(id)
        consumer.fullname = request.json.get('fullname')
        consumer.phone_number = request.json.get('phone_number')
        consumer.address = request.json.get('address')

        db.session.commit()

        return jsonify(consumer.serialize()), 200

    if request.method == 'DELETE':
        consumer = Consumer.query.get(id)
        db.session.delete(consumer)
        db.session.commit()

        return jsonify({'consumer':'Deleted'}), 200
    
    
        