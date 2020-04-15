from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, ConsumerBusiness

bcrypt = Bcrypt()
authconsumerbusiness = Blueprint('authconsumerbusiness', __name__)
@authconsumerbusiness.route('/authconsumerbusinesslogin', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        return jsonify({"msg": "You need insert your email"}), 422
    if not password:
        return jsonify({"msg": "You need insert your password"}), 422
    consumerbusiness = ConsumerBusiness.query.filter_by(email=email).first()
    if not consumerbusiness:
        return jsonify({"msg": "Email is not correct"}), 404
    pw_hash = bcrypt.generate_password_hash(password)
    if bcrypt.check_password_hash(consumerbusiness.password, password):
        access_token = create_access_token(identity=consumerbusiness.email)
        data = {
            "access_token": access_token,
            "consumerbusiness": consumerbusiness.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is not correct"}), 401
        
@authconsumerbusiness.route('/authconsumerbusinessregister', methods=['POST'])
def register():
    email = request.json.get('email')
    fullname = request.json.get('fullname')
    password = request.json.get('password')
    if not email:
        return jsonify({"msg": "You need to write yor email"}), 422
    if not fullname:
        return jsonify({"msg": "You need to write your name"}), 422             
    if not password:
        return jsonify({"msg": "You need to write your password"}), 422
    consumerbusiness = ConsumerBusiness.query.filter_by(email=email).first()
    if consumerbusiness:
        return jsonify({"msg": "This email already exist"}), 422
    consumerbusiness = ConsumerBusiness()
    consumerbusiness.email = email
    consumerbusiness.fullname = fullname
    consumerbusiness.password = bcrypt.generate_password_hash(password)
    db.session.add(consumerbusiness)
    db.session.commit()
    if bcrypt.check_password_hash(consumerbusiness.password, password):
        access_token = create_access_token(identity=consumerbusiness.email)
        data = {
            "access_token": access_token,
            "business": consumerbusiness.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is incorrect"}), 401