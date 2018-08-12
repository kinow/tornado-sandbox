import tornado.ioloop
import tornado.web

import sqlalchemy
import sqlite3

conn = sqlite3.connect('posts.db')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class PostsHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("posts")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/posts", PostsHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
