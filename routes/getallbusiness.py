from flask import Blueprint, request, jsonify
from models import db, Negocio

route_businessesall = Blueprint('route_businessesall', __name__)

@route_businessesall.route('/businessesall', methods = ['GET'])
#@route_businesses.route('/businesses/<int:id>', methods = ['GET', 'PUT', 'DELETE'])

def businessesall():
    if request.method == 'GET':
        negocios = Negocio.query.all()
        negocios = list(map(lambda negocio: negocio.serialize(), negocios))
        return jsonify(negocios), 200

   
        