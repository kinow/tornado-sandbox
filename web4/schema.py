import graphene
import datetime


class Fruit(graphene.ObjectType):
    name = graphene.String()
    date = graphene.String()


class Query(graphene.ObjectType):

    fruit = graphene.Field(Fruit)

    def resolve_fruit(self, info):
        return Fruit(name="Banana", date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z"))

schema = graphene.Schema(query=Query)
