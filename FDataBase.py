import math
import re
import sqlite3
import time

from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()

            if res:
                return res
        except:
            print('Error reading data from DB!')
        return []

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('The Article already exists...')
                return False

            base = url_for('static', filename='images/flask_intro/')

            text = re.sub(r'(?P<tag><img\s+[^>]*src=)(?P<quote>["\'])(?P<url>.+?)(?P<name>image\d{3}\.jpg)(?P=quote)>',
                          "\\g<tag>" + base + "\\g<name>>",
                          text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ? ,?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding article to DB " + str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:


                return res
        except sqlite3.Error as e:
            print('Error getting article from DB' + str(e))
        return (False, False)

    def getPostsAnnonce(self):
        try:
            self.__cur.execute(f'SELECT id, title, url, text FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Error getting article from DB ' + str(e))

        return []
