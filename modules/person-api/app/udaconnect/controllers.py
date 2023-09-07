from datetime import datetime

from app.udaconnect.models import Person
from app.udaconnect.schemas import (
    # ConnectionSchema,
    PersonSchema,
)
from app.udaconnect.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

import grpc
import app.person_pb2 as person_pb2
import app.person_pb2_grpc as person_pb2_grpc

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa



# TODO: This needs better exception handling


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()

        channel = grpc.insecure_channel("person-service.default.svc.cluster.local:5005")
        stub = person_pb2_grpc.PersonServiceStub(channel)

        response = stub.Create(person_pb2.PersonMessage(**payload))
        person: Person = Person()
        person.id = response.id
        person.first_name = response.first_name
        person.last_name  = response.last_name
        person.company_name = response.company_name
        # person: Person = PersonService.create(payload)
        # person = person_pb2.PersonMessage(
        #     id=payload.id,
        #     first_name=payload.first_name,
        #     last_name=payload.last_name,
        #     company_name=payload.company_name
        # )
        # channel = grpc.insecure_channel("localhost:5005")
        # stub = person_pb2_grpc.PersonServiceStub(channel)
        # response = stub.Create(person)
        # person: Person = Person()
        # person.first_name = response["id"]
        # person.first_name = response["first_name"]
        # person.last_name = response["last_name"]
        # person.company_name = response["company_name"] 
        return person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        # persons: List[Person] = PersonService.retrieve_all()
        channel = grpc.insecure_channel("person-service.default.svc.cluster.local:5005")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        # response = stub.Get(person_pb2.Empty())
        # persons: List[Person] = [{
        response = stub.Get(person_pb2.Empty())
        print(response)
        print("persons response")
        print(response.persons)
        # } for person in response]
        persons: List[Person] = []
        for person_msg in response.persons:
            person = Person()
            person.id = person_msg.id
            person.first_name = person_msg.first_name
            person.last_name = person_msg.last_name
            person.company_name = person_msg.company_name
            persons.append(person)
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        # person: Person = PersonService.retrieve(person_id)
        # channel = grpc.insecure_channel("localhost:5005")
        channel = grpc.insecure_channel("person-service.default.svc.cluster.local:5005")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        print(person_id)
        id_ = int(person_id)
        print(id_)
        personIdMessage = person_pb2.PersonIdMessage(id=id_)
        print(personIdMessage)
        response = stub.GetPerson(personIdMessage)
        print(response)
        aPerson: Person = Person()
        aPerson.id = response.id
        aPerson.first_name = response.first_name
        aPerson.last_name = response.last_name
        aPerson.company_name = response.company_name
        return aPerson


# @api.route("/persons/<person_id>/connection")
# @api.param("start_date", "Lower bound of date range", _in="query")
# @api.param("end_date", "Upper bound of date range", _in="query")
# @api.param("distance", "Proximity to a given user in meters", _in="query")
# class ConnectionDataResource(Resource):
#     @responds(schema=ConnectionSchema, many=True)
#     def get(self, person_id) -> ConnectionSchema:
#         start_date: datetime = datetime.strptime(
#             request.args["start_date"], DATE_FORMAT
#         )
#         end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
#         distance: Optional[int] = request.args.get("distance", 5)

#         results = ConnectionService.find_contacts(
#             person_id=person_id,
#             start_date=start_date,
#             end_date=end_date,
#             meters=distance,
#         )
#         return results
