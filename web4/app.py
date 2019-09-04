from asyncio import Queue

import tornado.web
import tornado.websocket
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from graphql_ws.constants import GRAPHQL_WS
from tornado.ioloop import IOLoop

from schema import schema
from template import render_graphiql
from tornado_ws_wip import TornadoSubscriptionServer


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish(render_graphiql())


class SubscriptionHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, sub_server):
        self.subscription_server = sub_server
        self.queue = Queue(100)

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    def open(self, *args, **kwargs):
        IOLoop.current().spawn_callback(subscription_server.handle, self)

    async def on_message(self, message):
        await self.queue.put(message)

    async def recv(self):
        return await self.queue.get()


subscription_server = TornadoSubscriptionServer(schema)


class GraphQLApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/graphql$', TornadoGraphQLHandler, dict(schema=schema)),
            (r'/graphql/batch', TornadoGraphQLHandler,
             dict(schema=schema, batch=True)),
            (r'/graphiql$', GraphiQLHandler),
            (r'/subscriptions', SubscriptionHandler,
             dict(sub_server=subscription_server))
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


if __name__ == '__main__':
    app = GraphQLApplication()
    app.listen(5000)
    IOLoop.instance().start()
