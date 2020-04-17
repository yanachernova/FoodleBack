from flask import Blueprint, request, jsonify
from models import db, Consumer
from flask_bcrypt import Bcrypt
from libs.functions import sendMail
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
bcrypt = Bcrypt()
route_changepasscostumers = Blueprint('route_changepasscostumers', __name__)
@route_changepasscostumers.route('/change-password', methods=['PUT'])
@jwt_required
def changepassword():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON request"}), 400
    password = request.json.get('password', None)
    if not password or password == '':
        return jsonify({"msg": "Missing password request"}), 400
    email = get_jwt_identity()
    consumer = Consumer.query.filter_by(email=email).first()
    consumer.password = bcrypt.generate_password_hash(password)

    sendMail('Password changed!!','Yana','fineukraine94@gmail.com','sacm1046@gmail.com')

    db.session.commit()
    return jsonify({"msg": "password has changed"}), 200
