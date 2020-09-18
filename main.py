import flask
import configparser
from static import static
from session import session
from dbquery import dbquery
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
    #connection to db
    dbLogin=''
    dbPassword=''
    try:
        dbLogin=os.environ['DatabaseLogin']
        dbPassword=os.environ['DatabasePassword']
    except KeyError:
        print('Please define environment variable DatabaseLogin and DatabasePassword')
        sys.exit(1)
    db=pymysql.connect(host=dbAddr, port=int(dbPort), user=dbLogin, password=dbPassword, db='fictionalinvention')
    cursor=db.cursor()
    app.config['db']=db
    app.config["cursor"]=cursor
    #secret key for JWT signing
    secretKey=os.urandom(64).hex()
    app.config["secretKey"]=secretKey

    app.register_blueprint(static)
    app.register_blueprint(session)
    app.register_blueprint(dbquery)
    app.run(host=appHost, port=int(appPort))