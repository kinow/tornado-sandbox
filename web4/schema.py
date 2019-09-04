import asyncio
import graphene
import datetime
from rx import Observable


class Fruit(graphene.ObjectType):
    name = graphene.String()
    date = graphene.String()


class Query(graphene.ObjectType):

    fruit = graphene.Field(Fruit)

    async def resolve_fruit(self, info):
        return Fruit(name="Banana", date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z"))


class Subscription(graphene.ObjectType):

    fruit = graphene.Field(Fruit)
    fruit2 = graphene.Field(Fruit)

    def resolve_fruit(self, info):
        # while True:
        #     yield Fruit(name="Banana", date=datetime.datetime.now().strftime(
        #         "%Y-%m-%d %H:%M:%S%z"))
        #     await asyncio.sleep(1.)
        fruit = Fruit(name="Banana", date=datetime.datetime.now().strftime(
                 "%Y-%m-%d %H:%M:%S%z"))
        return Observable.from_([fruit]).map(lambda x: x)
        #return fruit

    async def resolve_fruit2(root, info):
        while True:
            yield Fruit(name="Banana", date=datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S%z"))
            await asyncio.sleep(1.)


schema = graphene.Schema(query=Query, subscription=Subscription)
