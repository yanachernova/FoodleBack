from flask import jsonify
from flask_mail import Mail, Message
mail = Mail()

def sendMail(subject, name, from_email, to_email):
    msg = Message(subject, sender=[name, from_email], recipients=[to_email])
    msg.html = '<h1>Password Changed</h1>'
    mail.send(msg)
    return jsonify({"msg": "Email send successfully"}), 200