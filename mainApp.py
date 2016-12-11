import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
from platform import system
import tornado.websocket
import json
import MySQLdb
from clientCareClass import userCare
import random




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/main.html")
i = 0
def getUID():
    global i
    i += 1
    return i

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        self.care = userCare(getUID(),db)
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
            "static_path": os.path.join(os.path.dirname(__file__),"views"),
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
        db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="",  # your password
                         db="ebayset")  # name of the data base
    except Exception as e:
        print(e)
        exit()
    return db
def getCat():
    curs = db.cursor()
    curs.execute("SELECT DISTINCT categoryId, categoryName FROM items;")
    a = curs.fetchall()
    return [list(x) for x in a]

if __name__ == "__main__":
    if system() in ["Windows", "Darwin"]:
        port = 8888
    else:
        port = 80
    db = connect()
    a = random.randint(0,400)
    categories = getCat()[a:a+104]
    app = make_app()
    app.listen(port)
    print("The server is UP and running after change")
    tornado.ioloop.IOLoop.current().start()