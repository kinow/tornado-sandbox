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
        IOLoop.current().spawn_callback(self.subscription_server.handle, self)

    async def on_message(self, message):
        await self.queue.put(message)

    async def recv(self):
        return await self.queue.get()

    def check_origin(self, origin: str) -> bool:
        return True


subscription_server = TornadoSubscriptionServer(schema)


class GraphQLHandler(TornadoGraphQLHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class GraphQLApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/graphql$', GraphQLHandler, dict(schema=schema)),
            (r'/graphql/batch', GraphQLHandler, dict(schema=schema, batch=True)),
            (r'/graphiql$', GraphiQLHandler),
            (r'/subscriptions', SubscriptionHandler, dict(sub_server=subscription_server))
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True, debug=True)


if __name__ == '__main__':
    app = GraphQLApplication()
    app.listen(5000)
    IOLoop.instance().start()
