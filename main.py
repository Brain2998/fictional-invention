import flask
import configparser
from static import static
from session import session
import pymysql
import os
import sys

app = flask.Flask(__name__)

if __name__ == "__main__":
    parser=configparser.ConfigParser()
    parser.read_file(open('config.ini', 'r'))
    appHost=parser.get('Common', 'APP_ADDRESS')
    appPort=parser.get('Common', 'APP_PORT')
    dbAddr=parser.get('DB', 'DB_ADDRESS')
    dbPort=parser.get('DB', 'DB_PORT')

    dbLogin=''
    dbPassword=''
    try:
        dbLogin=os.environ['DatabaseLogin']
        dbPassword=os.environ['DatabasePassword']
    except KeyError:
        print('Please define environment variable DatabaseLogin and DatabasePassword')
        sys.exit(1)
    db=pymysql.connect(dbAddr, int(dbPort), dbLogin, dbPassword, 'fictionalinvention')

    app.register_blueprint(static)
    app.register_blueprint(session)
    app.run(host=appHost, port=int(appPort))