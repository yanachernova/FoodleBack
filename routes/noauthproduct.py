from flask import Blueprint, request, jsonify
from models import db, Product

route_noauthproducts = Blueprint('route_noauthproducts', __name__)

@route_noauthproducts.route('/noauthproducts/categories/<int:category_id>', methods=['GET'])
@route_noauthproducts.route('/noauthproducts/negocios/<int:negocio_id>', methods=['GET'])

def products(id=None, category_id = None):
    if request.method == 'GET':
        if category_id is not None:
            products = Product.query.filter_by(category_id=category_id).all()
            products = list(map(lambda product: product.serialize(),products))
            return jsonify(products), 200

