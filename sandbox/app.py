
import os

import tornado.web
import tornado.ioloop
import tornado.locks

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler)
        ]
        settings = dict(
            app_title='Tornado Sandbox',
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass


class HomeHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("home.html")


async def main():
    tornado.options.parse_command_line()

    app = Application()
    app.listen(options.port)

    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)
