import flask
from flask import request

session=flask.Blueprint('Session', __name__)

@session.route('/login', methods=['POST'])
def auth():
    print(request.form)
    login=request.form['login']
    password=request.form['password']
    return flask.Response(status=200)