from flask import Blueprint, request, jsonify
from models import db, Product
from flask_jwt_extended import (
    jwt_required
)
sendemail = Blueprint('sendemail', __name__)
@sendemail.route('/sendemail', methods=['POST'])
def sendemail():
    subject = request.json.get('subject', None)
    to_email = 'fineukraine94@gmail.com'
    name = request.json.get('name', None)
    from_email = request.json.get('from', None)
    message = request.json.get('message', None)

    if not subject:
        return jsonify({"subject": "Subject is required"}), 422
    if not name:
        return jsonify({"name": "Name is required"}), 422
    if not from_email:
        return jsonify({"from": "From is required"}), 422
    if not message:
        return jsonify({"message": "Message is required"}), 422

    msg = Message(subject, sender=[name, from_email], recipients=[to_email])
    msg.body = message
    mail.send(msg)

    return jsonify({"msg": "Email send successfully"}), 200

