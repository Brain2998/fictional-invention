import flask
import jwt
from session import require_auth

static=flask.Blueprint('static', __name__)

@static.route('/')
def index():
    return flask.send_from_directory('.', 'static/login.html')

@static.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('static/js', path)

@static.route('/css/<path:path>')
def send_css(path):
    return flask.send_from_directory('static/css', path)

@static.route('/home')
@require_auth
def gohome():
    token=flask.request.cookies.get('token')
    payload=jwt.decode(token, verify=False)
    if payload['role']=='Administrator':
        return flask.send_from_directory('.', 'static/servers.html')
    elif payload['role']=='User':
        return flask.send_from_directory('.', 'static/books.html')
    else:
        return flask.redirect('/', code=302)