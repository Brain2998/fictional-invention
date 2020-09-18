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
    name=flask.request.form['name']
    author=flask.request.form['author']
    genre=flask.request.form['genre']
    cursor=flask.current_app.config['cursor']
    cursor.execute("INSERT INTO books (`name`, `author`, `genre`) VALUES (%s, %s, %s)", (name, author, genre))
    flask.current_app.config['db'].commit()
    return flask.Response(status=200)

@dbquery.route('/editBook', methods=["POST"])
@require_auth
@require_role('User')
def editBook():
    id=flask.request.form['id']
    name=flask.request.form['name']
    author=flask.request.form['author']
    genre=flask.request.form['genre']
    cursor=flask.current_app.config['cursor']
    cursor.execute("UPDATE books SET `name`=%s, `author`=%s, `genre`=%s WHERE id=%s", (name, author, genre, id))
    return flask.Response(status=200)

@dbquery.route('/deleteBook', methods=["POST"])
@require_auth
@require_role('User')
def deleteBook():
    id=flask.request.form['id']
    cursor=flask.current_app.config['cursor']
    cursor.execute("DELETE FROM books WHERE id=%s", id)
    flask.current_app.config['db'].commit()
    return flask.Response(status=200)


@dbquery.route('/getServersList')
@require_auth
@require_role('Administrator')
def getServersList():
    cursor=flask.current_app.config['cursor']
    cursor.execute("SELECT * FROM servers")
    rows=cursor.fetchall()
    result=[]
    for r in rows:
        result.append({'id': r[0],'name': r[1], 'processor': r[2], 'ram': r[3], 'system': r[4]})
    return flask.Response(json.dumps(result))

@dbquery.route('/addNewServer', methods=['POST'])
@require_auth
@require_role('Administrator')
def addNewServer():
    name=flask.request.form['name']
    processor=flask.request.form['processor']
    ram=flask.request.form['ram']
    system=flask.request.form['system']
    cursor=flask.current_app.config['cursor']
    cursor.execute("INSERT INTO servers (`name`, `processor`, `ram`, `system`) VALUES (%s, %s, %s, %s)", (name, processor, ram, system))
    flask.current_app.config['db'].commit()
    return flask.Response(status=200)

@dbquery.route('/editServer', methods=["POST"])
@require_auth
@require_role('Administrator')
def editServer():
    id=flask.request.form['id']
    name=flask.request.form['name']
    processor=flask.request.form['processor']
    ram=flask.request.form['ram']
    system=flask.request.form['system']
    cursor=flask.current_app.config['cursor']
    cursor.execute("UPDATE servers SET `name`=%s, `processor`=%s, `ram`=%s, `system`=%s WHERE id=%s", (name, processor, ram, system, id))
    return flask.Response(status=200)

@dbquery.route('/deleteServer', methods=["POST"])
@require_auth
@require_role('Administrator')
def deleteServer():
    id=flask.request.form['id']
    cursor=flask.current_app.config['cursor']
    cursor.execute("DELETE FROM servers WHERE id=%s", id)
    flask.current_app.config['db'].commit()
    return flask.Response(status=200)