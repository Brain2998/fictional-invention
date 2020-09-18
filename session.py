import flask
from flask import request, current_app
from passlib.hash import pbkdf2_sha512
import jwt
import datetime
import time

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
        response=flask.make_response(flask.redirect('/home', code=302))
        response.set_cookie('token', value=token, max_age=1800, secure=True, httponly=True)
        #Log
        cursor.execute("INSERT INTO events (`user`, `action`, `time`) VALUES (%s, %s, %s)", (login, 'authenticated', time.strftime('%Y-%m-%d %H:%M:%S')))
        flask.current_app.config['db'].commit()
        return response
    else:
        #Log
        cursor.execute("INSERT INTO events (`user`, `action`, `time`) VALUES (%s, %s, %s)", (login, 'not authenticated', time.strftime('%Y-%m-%d %H:%M:%S')))
        flask.current_app.config['db'].commit()
        return flask.Response('Invalid user or password', status=401)

@session.route('/logout')
def logout():
    response=flask.make_response(flask.redirect('/', code=302))
    response.set_cookie('token', value='', max_age=1800, secure=True, httponly=True)
    #Log
    cursor=current_app.config['cursor']
    token=request.cookies.get('token')
    payload=jwt.decode(token, verify=False)
    cursor.execute("INSERT INTO events (`user`, `action`, `time`) VALUES (%s, %s, %s)", (payload['username'], 'logged out', time.strftime('%Y-%m-%d %H:%M:%S')))
    flask.current_app.config['db'].commit()
    return response

def require_auth(func):
    def decorate(*args, **kwargs):
        token=request.cookies.get('token')
        secretKey=current_app.config['secretKey']
        try:
            jwt.decode(token, secretKey, algorithms=['HS256'])
        except:
            return flask.redirect('/', code=302)
        return func(*args, **kwargs)
    decorate.__name__ = func.__name__
    return decorate

def require_role(role):
    def innerDecorator(func):
        def decorate(*args, **kwargs):
            token=request.cookies.get('token')
            payload=jwt.decode(token, verify=False)
            if (role!=payload['role']):
                return flask.redirect('/', code=302)
            return func(*args, **kwargs)
        decorate.__name__ = func.__name__
        return decorate
    return innerDecorator
