import os

import tornado.ioloop
import tornado.web

import json

import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import inspect
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


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
        session = DBSession()
        posts = session.query(Post).all()
        self.write("{}".format(len(posts)))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/posts$", PostsHandler)
    ])

if __name__ == "__main__":
    engine = create_engine('sqlite:///posts.db')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    if not os.path.isfile('posts.db'):
	    session = DBSession()

	    new_user = User(name="john", passwd="foo")
	    session.add(new_user)
	    session.commit()

	    new_post1 = Post(text="This is a test", user_id=new_user.id)
	    new_post2 = Post(text="This is a text", user_id=new_user.id)
	    session.add(new_post1)
	    session.add(new_post2)
	    session.commit()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
