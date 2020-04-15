from flask import Blueprint, request, jsonify
from models import db, Driver
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required
)
bcrypt = Bcrypt()
route_drivers = Blueprint('route_drivers', __name__)
@route_drivers.route('/drivers', methods=['GET'])
@route_drivers.route('/drivers/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def drivers(id=None):
    if request.method == 'GET':
        if id is not None:
            driver = Driver.query.get(id)
            if driver:
                return jsonify(driver.serialize()), 200
            else:
                return jsonify({"driver":"Not found"}), 404
        else:
            drivers = Driver.query.all()
            drivers = list(map(lambda driver: driver.serialize(),drivers))
            return jsonify(drivers), 200
    
    if request.method == 'PUT':
        driver = Driver.query.get(id)
        driver.fullname = request.json.get('fullname')
        driver.email = request.json.get('email')
        driver.password = request.json.get('password')
        driver.address = request.json.get('address')
        driver.phone_number = request.json.get('phone_number')
        db.session.commit()
        return jsonify(driver.serialize()), 200
    if request.method == 'DELETE':
        driver = Driver.query.get(id)
        db.session.delete(driver)
        db.session.commit()
        return jsonify({'driver':'Deleted'}), 200