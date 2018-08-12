import tornado.ioloop
import tornado.web

import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    passwd = Column(String(200))

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

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
    engine = create_engine('sqlite:///sqlalchemy_example.db')
    Base.metadata.create_all(engine)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
