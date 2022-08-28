import sqlite3
import os
from flask import Flask, render_template, request, g, url_for, flash, abort
from FDataBase import FDataBase

# CONFIG for SQLite in FLASK
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'qwefsdfwe34wedasdffasdf'

app = Flask(__name__)
app.config.from_object(__name__)  # loading CONFIG from our app

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))  # update CONFIG - path to DB file


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():  # create TABLES in DB
    '''Method for creating of DB'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# g - during connction request it is creating application context vith global variable g.
# we may push any our (user) information to this variabe of current request
# g should be imported from flask as g now lives in the application context.
# Every request pushes a new application context  - g

def get_db():  # connect to db on connection request
    """Connect to DB if not yet connected"""
    if not hasattr(g, 'link_db'):  # check if g has attribute 'link_db', if no ...
        g.link_db = connect_db()  # then we will connect to db and set variable g to has attribute 'link_db'
    return g.link_db


@app.teardown_request  # activation on destroing of application context (it is happening in the moment of handling of request
def close_db(error):
    '''close connection with db, if its exists'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnnonce())


@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Article adding error', category='error')
            else:
                flash('Article added successfully', category='success')
        else:
            flash('Article adding error', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Article adding')


@app.route('/post/<alias>')
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
