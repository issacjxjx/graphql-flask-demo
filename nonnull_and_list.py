import datetime
import graphene

from flask import Flask
from flask_graphql import GraphQLView
from graphql.language import ast


class MyDateTime(graphene.Scalar):
    '''
    custom datetime type
    '''

    @staticmethod
    def serialize(date_time):
        '''serialize'''
        return date_time.isoformat()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(node.value, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

class Resp(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.NonNull(graphene.String) # equivalent to: name = graphene.String(required=True)
    age = graphene.Int()
    now = MyDateTime()
    friends = graphene.List(graphene.String)
    
class Query(graphene.ObjectType):
    resp = graphene.Field(Resp)
    def resolve_resp(self, args, context, info):
        return Resp(id=1, name="foo", age=111, now=datetime.datetime.now(), friends=['John', 'Jane', 'Smith'])


app = Flask(__name__)
app.add_url_rule("/", view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query)))


if __name__ == '__main__':
    # curl -H 'Content-type: application/graphql' -d 'query {resp {id, name, age, now}}' http://localhost:5000/
    # {"data":{"resp":{"id":"1","name":"foo","age":111, "now": "2017-03-03T14:58:50.844666"}}}
    app.run()