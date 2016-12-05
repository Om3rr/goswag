import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os
from platform import system


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("views/main.html")


class Application(tornado.web.Application):
    code = None
    def __init__(self):
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "views")
        }
        handlers = [
            (r"/", MainHandler),
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