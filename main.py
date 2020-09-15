import flask
from static import static
from session import session
import pymysql

app = flask.Flask(__name__)

if __name__ == "__main__":
    db=pymysql.connect
    app.register_blueprint(static)
    app.register_blueprint(session)
    app.run(host="0.0.0.0", port=80)