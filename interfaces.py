import graphene

from flask import Flask
from flask_graphql import GraphQLView

class Person(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()


class Driver(graphene.ObjectType):
    class Meta:
        interfaces = (Person,)

    driver_license = graphene.String()



class Query(graphene.ObjectType):
    driver = graphene.Field(Driver)
    def resolve_driver(self, args, context, info):
        return Driver(id=1, name="foo", age=111, driver_license="foo license")


app = Flask(__name__)
app.add_url_rule("/", view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query)))


if __name__ == '__main__':
    # curl -H 'Content-type: appliion/graphql' -d 'query {driver {id, name, age, driverLicense}}' http://localhost:5000/
    # {"data":{"driver":{"id":"1","name":"foo","age":111,"driverLicense":"foo license"}}}
    app.run()