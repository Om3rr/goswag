import tornado.ioloop
import tornado.web
import tornado.auth
import os.path, os


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
