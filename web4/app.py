from asyncio import Queue

import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop

from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from graphene_tornado.tornado_executor import TornadoExecutor
from tornado_ws_wip import TornadoSubscriptionServer

#from graphiql_template_vue import render_graphiql
from template import render_graphiql
from graphql_ws.constants import GRAPHQL_WS

from schema import schema


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish(render_graphiql())

## to render a Vue app with GraphiQL
#class GraphiQLHandler(tornado.web.RequestHandler):
#    def get(self):
#        self.finish(render_graphiql())


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
        executor = TornadoExecutor()
        # graphql Executor now needs a `allow_subscriptions=True`, or you will get
        # {
        #   "errors": [
        #     {
        #       "message": "Subscriptions are not allowed. You will need to either use the subscribe function or pass allow_subscriptions=True"
        #     }
        #   ],
        #   "data": null
        # }
        #executor.allow_subscriptions = True
        handlers = [
            #(r'/graphql', TornadoGraphQLHandler, dict(graphiql=True, schema=schema, executor=executor, allow_subscriptions=True)),
            #(r'/graphql/batch', TornadoGraphQLHandler, dict(graphiql=True, schema=schema, batch=True, executor=executor, allow_subscriptions=True)),
            #(r'/graphql/graphiql', GraphiQLHandler, dict(graphiql=True, schema=schema, executor=executor, allow_subscriptions=True)),
            #(r'/subscriptions', SubscriptionHandler)
            (r'/graphql$', TornadoGraphQLHandler, dict(schema=schema)),
            (r'/graphql/batch', TornadoGraphQLHandler, dict(schema=schema, batch=True)),
            (r'/graphiql$', GraphiQLHandler),
            (r'/subscriptions', SubscriptionHandler, dict(sub_server=subscription_server))
        ]
        tornado.web.Application.__init__(self, handlers, autoreload=True)


if __name__ == '__main__':
    app = GraphQLApplication()
    app.listen(5000)
    IOLoop.instance().start()
