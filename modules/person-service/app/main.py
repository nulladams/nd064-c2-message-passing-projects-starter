import logging
from datetime import datetime, timedelta
from typing import Dict, List
import os

# from app import db

import time
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc

import psycopg2

from sqlalchemy import create_engine


#from app.udaconnect.models import Connection, Location, Person
from models import Person
#from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from schemas import PersonSchema
from services import PersonService
#from geoalchemy2.functions import ST_AsText, ST_Point
#from sqlalchemy.sql import text

#from app import create_app
from config import config_by_name
env = os.getenv("FLASK_ENV") or "test"
print(config_by_name[env or "test"])
#app = create_app(os.getenv("FLASK_ENV") or "test")
#con = psycopg2.connect(host='localhost', database='regiao'

logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger("udaconnect-api")

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

print(DB_USERNAME+DB_HOST+DB_PORT)

# engine = create_engine("sqlite://", echo=True, future=True)
# engine = create_engine(
#     "postgresql+pg8000://scott:tiger@localhost/test",
# )
###
print("will create engine")
logging.info("will create engine")
engine = create_engine(
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("engine created")
###

# class PersonService:
#     @staticmethod
#     def create(person: Dict) -> Person:
#         new_person = Person()
#         new_person.first_name = person["first_name"]
#         new_person.last_name = person["last_name"]
#         new_person.company_name = person["company_name"]

#         db.session.add(new_person)
#         db.session.commit()

#         return new_person

#     @staticmethod
#     def retrieve(person_id: int) -> Person:
#         person = db.session.query(Person).get(person_id)
#         return person

#     @staticmethod
#     def retrieve_all() -> List[Person]:
#         return db.session.query(Person).all()


class PersonServicer(person_pb2_grpc.PersonServiceServicer):

    def Get(self, request, context):

        # request_value = {
        #     "id": request.id,
        #     "first_name": request.first_name,
        #     "last_name": request.last_name,
        #     "company_name": request.company_name
        # }

        #request_value = PersonService.retrieve_all()

        #print(request_value)
        first_value = {
            "id": 1,
            "first_name": "dani",
            "last_name": "adams",
            "company_name": "padocalab"
        }

        sec_value = {
            "id": 4,
            "first_name": "joana",
            "last_name": "adams",
            "company_name": "agro adams"
        }

        result = person_pb2.PersonMessageList()

        persons: List[Person] = PersonService.retrieve_all()
        print(persons)
        print(persons[0])
        logging.info("persons")
        logging.info(persons)
        print(persons[0].serialize)
        # for person in persons:
        #     print(f"{person.id} - {person.first_name} ")
        persons_arr = [person_pb2.PersonMessage(**person.serialize) for person in persons]
        #print(persons_arr)
        first_person = persons[0]
        print("id ", first_person.id)
        print("first ", first_person.first_name)

        result.persons.extend(persons_arr)


        # result.persons.extend([
        #         person_pb2.PersonMessage(**first_value), 
        #         person_pb2.PersonMessage(**sec_value)
        #         ])
        # result.persons.extend(persons)

        return result


    def GetPerson(self, request, context):

        print("request")
        print(request)
        print(request.id)
        person: Person = PersonService.retrieve(request.id)

        print(person.serialize)
        return person_pb2.PersonMessage(**person.serialize)


    def Create(self, request, context):

        # request_value = {
        #     "id": request.id,
        #     "first_name": request.first_name,
        #     "last_name": request.last_name,
        #     "company_name": request.company_name
        # }
        request_value = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }
        print(request)
        new_person: Person = PersonService.create(request_value)
        # PersonService.create(new_person)
        print(new_person)
        logging.info("new person")
        logging.info(new_person)
        print("Receive a message")

        #request_value = PersonService.retrieve_all()
        
        
        print(request_value)
        logging.info(request_value)
        #result = person_pb2.PersonMessageList()
        #result.orders.extend(request_value)

        #return result
        return person_pb2.PersonMessage(**request_value)




# app = create_app(os.getenv("FLASK_ENV") or "test")

# if __name__ == "__main__":
#     app.run(debug=True)

###
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

print("Server starting on port 5005")
logging.info("Server starting on port 5005")
###
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()

# try:
#     while True:
#         time.sleep(86400)
# except KeyboardInterrupt:
#     server.stop(0)