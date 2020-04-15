from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, Driver
bcrypt = Bcrypt()
authdriver = Blueprint('authdriver', __name__)
@authdriver.route('/logindriver', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        return jsonify({"msg": "Email is required"}), 422
    if not password:
        return jsonify({"msg": "Password is required"}), 422
    driver = Driver.query.filter_by(email=email).first()
    if not driver:
        return jsonify({"msg": "Email is not found"}), 404
    pw_hash = bcrypt.generate_password_hash(password)
    if bcrypt.check_password_hash(driver.password, password):
        access_token = create_access_token(identity=driver.email)
        data = {
            "access_token": access_token,
            "driver": driver.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password is incorrect"}), 401
        
@authdriver.route('/registerdriver', methods=['POST'])
def register():
    fullname = request.json.get('fullname')
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"msg": "Email is required"}), 422
    if not fullname:
        return jsonify({"msg": "Name is required"}), 422             
    if not password:
        return jsonify({"msg": "Password is required"}), 422
    driver = Driver.query.filter_by(email=email).first()
    if driver:
        return jsonify({"msg": "This email already register"}), 422
    driver = Driver()
    driver.email = email
    driver.fullname = fullname
    driver.password = bcrypt.generate_password_hash(password)
    db.session.add(driver)
    db.session.commit()
    if bcrypt.check_password_hash(driver.password, password):
        access_token = create_access_token(identity=driver.email)
        data = {
            "access_token": access_token,
            "consumer": driver.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "Email or password incorrect"}), 401