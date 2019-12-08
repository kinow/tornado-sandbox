import asyncio
import datetime
import graphene
from promise import Promise

from rx import Observable, AnonymousObservable


class Fruit(graphene.ObjectType):
    name = graphene.String()
    date = graphene.String()


class Query(graphene.ObjectType):
    fruit = graphene.Field(Fruit)

    def resolve_fruit(self, info):
        banana = Fruit(name="Banana", date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z"))
        obs = Observable.from_([banana])  # type: AnonymousObservable
        return Promise(lambda resolve, reject: resolve(obs))

class Subscription(graphene.ObjectType):
    fruit = graphene.Field(Fruit)

    async def resolve_fruit(root, info):
        while True:
            yield Fruit(name="Banana", date=datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S%z"))
            await asyncio.sleep(1.)


schema = graphene.Schema(query=Query, subscription=Subscription)
