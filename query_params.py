import datetime
import graphene

from flask import Flask
from flask_graphql import GraphQLView

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

class Person(graphene.Interface):
    name = graphene.String()
    age = graphene.Int()
    gender = graphene.String()

class Employee(graphene.ObjectType):
    class Meta:
        interfaces = (Person,)

    id = graphene.ID()
    dept = graphene.String()

class Company(graphene.ObjectType):
    birthday = MyDateTime()
    name = graphene.String()
    license = graphene.String()
    employees = graphene.List(Employee, id=graphene.Int())

    def resolve_company(self, args, context, info):
        print('args: {0}'.format(args))
        return self.employees




class Query(graphene.ObjectType):
    company = graphene.Field(Company)
    def resolve_company(self, args, context, info):
        print('args: {0}'.format(args))
        employees = [Employee(id=1, name="name1", age=44, gender="male", dept="sales"), Employee(id=2, name="name2", age=44, gender="female", dept="R&D")]
        
        return Company(birthday=datetime.datetime.now(), name="gs", license="0000000", employees=employees)


app = Flask(__name__)
app.add_url_rule("/", view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query)))


if __name__ == '__main__':
    # curl -H 'Content-type: application/graphql' -d 'query {company   {birthday, name, license, employees (id: 1) { age  }}}' http://localhost:5000/
    # {"data":{"company":{"birthday":"2017-03-03T20:38:07.285602","name":"gs","license":"0000000","employees":[{"age":44},{"age":44}]}}}
    app.run()