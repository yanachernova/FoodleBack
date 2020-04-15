from flask import Blueprint, request, jsonify
from models import db, ConsumerBusiness
from flask_bcrypt import Bcrypt
from flask_jwt_extended import(
    jwt_required
)
bcrypt = Bcrypt()
route_consumerbusinesses = Blueprint('route_consumerbusinesses', __name__)

@route_consumerbusinesses.route('/consumerbusinesses', methods = ['GET'])
@route_consumerbusinesses.route('/consumerbusinesses/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
@jwt_required
def consumerbusinesses(id = None):
    if request.method == 'GET':
        if id is not None:
            consumerbusiness = ConsumerBusiness.query.get(id)
            if consumerbusiness:
                return jsonify(consumerbusiness.serialize()), 200
            else:
                return jsonify({"consumerbusiness": "Not found"}), 404
        else:
            consumerbusinesses = ConsumerBusiness.query.all()
            consumerbusinesses = list(map(lambda consumerbusiness: consumerbusiness.serialize(), consumerbusinesses))
            return jsonify(consumerbusinesses), 200

    if request.method == 'PUT':
        consumerbusiness = ConsumerBusiness.query.get(id)
        consumerbusiness.fullname = request.json.get('fullname')
        consumerbusiness.email = request.json.get('email')
        consumerbusiness.password = request.json.get('password')
        consumerbusiness.phone_number = request.json.get('phone_number')

        db.session.commit()

        return jsonify(consumerbusiness.serialize()), 200

    if request.method == 'DELETE':
        consumerbusiness = ConsumerBusiness.query.get(id)
        db.session.delete(consumerbusiness)
        db.session.commit()

        return jsonify({'consumerbusiness':'Deleted'}), 200
        