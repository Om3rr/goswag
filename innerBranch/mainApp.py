import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
from platform import system
import tornado.websocket
import json
import MySQLdb
from clientCareClass import userCare
from clientCareClass import categoryBrowser, dbWrapper
import random
import pickle
from algush import graphManager, soupFacade



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("../views/main.html")
i = 0
def getUID():
    global i
    i += 1
    return i
import time
class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        self.care = userCare(getUID(),db,cat,graph)
        print ("WebSocket opened")

        self.write_message(json.dumps(categories))

    def on_message(self, message):
        s = message.split(',')
        msgToSend = self.care.getMsg(s)
        if(msgToSend == 'returnCategories'):
            self.write_message(json.dumps(categories))
        self.write_message(json.dumps(msgToSend))

    def on_close(self):
        print ("WebSocket closed")


class Application(tornado.web.Application):
    code = None
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join('os.path.dirname(__file__)',"views"),
        }
        handlers = [
            (r"/", MainHandler),
            (r"/scores", MainHandler),
            (r"/websocket", EchoWebSocket),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

def make_app():
    return Application()
def connect():
    try:
        db = MySQLdb.connect(host='localhost',  # your host, usually localhost
                         user='root',  # your username
                         passwd='20403472',  # your password
                         db='ebayset')  # name of the data base
    except Exception as e:
		print('yo')
        print(e)
        exit()
    return db

def loadCategories():
    with open('categoriesNew','rb') as f:
        file = pickle.load(f)
        print("Categories load successfuly")
    return file
def getCat():
    curs = db.cursor()
    curs.execute("SELECT DISTINCT categoryId, categoryName FROM items;")
    a = curs.fetchall()
    return [list(x) for x in a]
import datetime


if __name__ == "__main__":
    if system() in ["Windows", "Darwin"]:
        port = 8888
    else:
        port = 80
    db = connect()
    print('db loaded')
    cat = categoryBrowser(loadCategories())
    categories = cat.getMainCat()
    graph = graphManager(dbWrapper(db))
    app = make_app()
    app.listen(port)
    print("The server is UP and running after change")
    current = tornado.ioloop.IOLoop.instance()
    current.add_timeout(datetime.timedelta(seconds=30), lambda:graph.pickleSave())
    current.start()