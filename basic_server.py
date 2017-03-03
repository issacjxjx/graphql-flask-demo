import graphene

from flask import Flask
from flask_graphql import GraphQLView

class Resp(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()
    

class Query(graphene.ObjectType):
    resp = graphene.Field(Resp)
    def resolve_resp(self, args, context, info):
        return Resp(id=1, name="foo", age=111)


app = Flask(__name__)
app.add_url_rule("/", view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query)))


if __name__ == '__main__':
    # curl -H 'Content-type: application/graphql' -d 'query {resp {id, name, age}}' http://localhost:5000/
    # {"data":{"resp":{"id":"1","name":"foo","age":111}}}
    app.run()

    