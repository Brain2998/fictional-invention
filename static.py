import flask

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