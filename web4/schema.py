import asyncio
import datetime

import graphene


class Fruit(graphene.ObjectType):
    name = graphene.String()
    date = graphene.String()


class Query(graphene.ObjectType):
    fruit = graphene.Field(Fruit)

    async def resolve_fruit(self, info):
        return Fruit(name="Banana", date=datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S%z"))


class Subscription(graphene.ObjectType):
    fruit = graphene.Field(Fruit)

    async def resolve_fruit(root, info):
        while True:
            yield Fruit(name="Banana", date=datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S%z"))
            await asyncio.sleep(1.)


schema = graphene.Schema(query=Query, subscription=Subscription)
