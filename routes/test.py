from flask import Flask,render_template,redirect,url_for,request,flash, Blueprint, jsonify
from flask_mail import Mail, Message
from libs.functions import sendMail
import random
from models import db, Consumer

route_test = Blueprint('route_test', __name__)

@route_test.route('/test',methods=["POST","GET"])
def test():
    if request.method=="POST":
        email = request.json.get('email')
        check = Consumer.query.filter_by(email=email).first()

        if check:
            def get_random_string(length=24,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
                return ''.join(random.choice(allowed_chars) for i in range(length))
            hashCode = get_random_string()
            check.hashCode = hashCode
            db.session.commit()
            sendMail('Confirm Password Change', 'Sebastián', 'fineukraine94@gmail.com', email,"Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode)
            return jsonify({"email":"sent successfully"}), 200 
    else:
        return jsonify({"email":"Not found"}), 400
    
"""@route_test.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('yanlış girdin')
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')

@route_test.route('/createUser')
def createUser():
    newUser = User(username='berat',mail='beratbozkurt1999@gmail.com',password='123456')
    db.session.add(newUser)
    db.session.commit()
    return "Created user"
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True) """