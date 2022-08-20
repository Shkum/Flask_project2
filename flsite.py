import sqlite3
import os
from flask import Flask, render_template, request

# CONFIG
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'qwefsdfwe34wedasdffasdf'

app = Flask(__name__)
app.config.from_object(__name__)  # loading CONFIG from our app

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))  # update CONFIG - path to DB file


def connect_db():
    conn = sqlite3.connect((app.config['DATABASE']))
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
