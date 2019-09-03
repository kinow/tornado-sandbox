import graphene


class Fruit(graphene.ObjectType):
    name = graphene.String()


class Query(graphene.ObjectType):

    fruit = graphene.Field(Fruit)

    def resolve_fruit(self, info):
        return Fruit(name="Banana")

schema = graphene.Schema(query=Query)
