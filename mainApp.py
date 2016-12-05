import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
from platform import system
import websocket
import asyncio
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/main.html")


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print ("WebSocket opened")

    def on_message(self, message):
        print(message)

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
            (r"/websocket", EchoWebSocket),
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def make_app():
    return Application()

if __name__ == "__main__":
    if system() in ["Windows", "Darwin"]:
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    print("The server is UP and running after change")
    tornado.ioloop.IOLoop.current().start()