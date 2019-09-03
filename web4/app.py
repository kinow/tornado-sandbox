from asyncio import Queue

import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop

from tornado_ws_wip import TornadoSubscriptionServer

# from graphene_tornado.schema import schema
from schema import schema
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler

subscription_server = TornadoSubscriptionServer(schema)


class SubscriptionHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, sub_server):
        self.subscription_server = subscription_server
        self.queue = Queue()

    def select_subprotocol(self, subprotocols):
        return 'graphql-ws'

    def open(self, *args, **kwargs):
        IOLoop.current().spawn_callback(subscription_server.handle, self)

    async def on_message(self, message):
        await self.queue.put(message)

    async def recv(self):
        return await self.queue.get()


class GraphQLApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/graphql', TornadoGraphQLHandler, dict(graphiql=True, schema=schema)),
            (r'/graphql/batch', TornadoGraphQLHandler, dict(graphiql=True, schema=schema, batch=True)),
            (r'/graphql/graphiql', TornadoGraphQLHandler, dict(graphiql=True, schema=schema)),
            (r'/subscriptions', SubscriptionHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


if __name__ == '__main__':
    app = GraphQLApplication()
    app.listen(5000)
    IOLoop.instance().start()
