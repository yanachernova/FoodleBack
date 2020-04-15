from flask import Blueprint, request, jsonify
from models import db, Negocio
from flask_jwt_extended import (
    jwt_required
)
route_negocios = Blueprint('route_negocios', __name__)
@route_negocios.route('/negocios', methods=['GET','POST'])
@route_negocios.route('/negocios/<int:id>', methods=['GET','PUT','DELETE'])
@route_negocios.route('/negocios/consumerbusiness/<int:consumerbusiness_id>', methods=['GET', 'POST'])
@route_negocios.route('/negocios/consumerbusiness/<int:consumerbusiness_id>/negocio/<int:id>', methods=['GET', 'POST'])
@jwt_required
def negocios(id=None, consumerbusiness_id = None):
    if request.method == 'GET':
        if id is not None and consumerbusiness_id is not None:
            negocio = Negocio.query.filter_by(consumerbusiness_id = consumerbusiness_id, id = id).first()
            if negocio:
                return jsonify(negocio.serialize()), 200
            else:
                return jsonify({"negocio":"Not found"}), 404
        elif id is not None:
            negocio = Negocio.query.get(id)
            if negocio:
                return jsonify(negocio.serialize()), 200
            else:
                return jsonify({"negocio": "Not found"})
        elif consumerbusiness_id is not None:
            negocios = Negocio.query.filter_by(consumerbusiness_id=consumerbusiness_id).all()
            negocios = list(map(lambda negocio: negocio.serialize(),negocios))
            return jsonify(negocios), 200
        else:
            negocios = Negocio.query.all()
            negocios = list(map(lambda negocio: negocio.serialize(),negocios))
            return jsonify(negocios), 200

    if request.method == 'POST':
        name = request.json.get('name')
        phone_number = request.json.get('phone_number')
        address = request.json.get('address')
        delivery_price = request.json.get('delivery_price')
        consumerbusiness_id = request.json.get('consumerbusiness_id')

        negocio = Negocio()
        negocio.name = name
        if not name:
            return jsonify({"name": "is required"}), 400
        negocio.phone_number = phone_number
        if not phone_number:
            return jsonify({"phone_number": "is required"}), 400
        negocio.address = address
        if not address:
            return jsonify({"address": "is required"}), 400
        negocio.delivery_price = delivery_price
        if not delivery_price:
            return jsonify({"delivery_price": "is required"}), 400
        negocio.consumerbusiness_id = consumerbusiness_id
        if not consumerbusiness_id:
            return jsonify({"consumerbusiness_id": "is required"}), 400
        db.session.add(negocio)
        db.session.commit()
        return jsonify(negocio.serialize()), 201
    
    if request.method == 'PUT':
  
        negocio = Negocio.query.get(id)
        negocio.name = request.json.get('name')
        negocio.address = request.json.get('address')
        negocio.phone_number = request.json.get('phone_number')
        negocio.delivery_price = request.json.get('delivery_price')
        db.session.commit()
        return jsonify(negocio.serialize()), 200

    if request.method == 'DELETE':
        
        negocio = Negocio.query.get(id)
        db.session.delete(negocio)
        db.session.commit()
        return jsonify({'negocio':'Deleted'}), 200