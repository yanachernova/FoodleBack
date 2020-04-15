from flask import Blueprint, request, jsonify
from models import db, Category

route_categoriesnoauth = Blueprint('route_categoriesnoauth', __name__)

@route_categoriesnoauth.route('/categoriesnoauth/negocios/<int:negocio_id>', methods=['GET'])

def categories(id=None, negocio_id = None):
    if request.method == 'GET':
        if negocio_id is not None:
            categories = Category.query.filter_by(negocio_id=negocio_id).all()
            categories = list(map(lambda category: category.serialize(),categories))
            return jsonify(categories), 200


    