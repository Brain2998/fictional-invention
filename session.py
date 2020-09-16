import flask
from flask import request, current_app
from passlib.hash import pbkdf2_sha512
import jwt
import datetime

session=flask.Blueprint('Session', __name__)

@session.route('/login', methods=['POST'])
def auth():
    login=request.form['login']
    password=request.form['password']
    cursor=current_app.config['cursor']
    cursor.execute("SELECT passwordhash, role FROM users WHERE username=%s", login)
    dbRecord=cursor.fetchone()
    if not dbRecord:
        return flask.Response('Invalid user or password', status=401)
    passwordHash=dbRecord[0]
    role=dbRecord[1]
    if pbkdf2_sha512.verify(password, passwordHash):
        secretKey=current_app.config['secretKey']
        token=jwt.encode({'username':login, 'role':role, 'exp': datetime.datetime.utcnow()+datetime.timedelta(seconds=1800)}, secretKey, algorithm='HS256')
        response=flask.make_response()
        response.set_cookie('token', value=token, max_age=1800, secure=True, httponly=True)
        return response
    else:
        return flask.Response('Invalid user or password', status=401)