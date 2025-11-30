import graphene


class UserType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)

    def resolve_viewer(self, info):
        # Just return a dict with the required fields
        return {"id": "user_123", "name": "Test User", "email": "test@example.com"}


schema = graphene.Schema(query=Query)
