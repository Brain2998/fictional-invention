import flask
from session import require_auth

home=flask.Blueprint('home', __name__)

@home.route('/home')
@require_auth
def gohome():
    return flask.Response(status=200)