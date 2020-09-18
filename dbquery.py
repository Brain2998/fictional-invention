import flask
from flask import request
from session import require_auth, require_role
import json

dbquery=flask.Blueprint('dbquery', __name__)

@dbquery.route('/getBooksList')
@require_auth
@require_role('User')
def getBooksList():
    cursor=flask.current_app.config['cursor']
    cursor.execute("SELECT * FROM books")
    rows=cursor.fetchall()
    result=[]
    for r in rows:
        result.append({'id': r[0],'name': r[1], 'author': r[2], 'genre': r[3]})
    return flask.Response(json.dumps(result))

@dbquery.route('/addNewBook', methods=['POST'])
@require_auth
@require_role('User')
def addNewBook():
    print(flask.request.form)
    name=flask.request.form['name']
    author=flask.request.form['author']
    genre=flask.request.form['genre']
    cursor=flask.current_app.config['cursor']
    cursor.execute('INSERT INTO books (name, author, genre) VALUES (%s, %s, %s)', (name, author, genre))
    flask.current_app.config['db'].commit()
    return flask.Response(status=200)
    #flask.make_response(flask.redirect('/home', code=302))