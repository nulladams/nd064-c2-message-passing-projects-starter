import logging
from datetime import datetime, timedelta
from typing import Dict, List
import os
import json

from kafka import KafkaConsumer

# from app import db

import time
from concurrent import futures

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

print("KAFKA")

# TOPIC_NAME = "persons"
# KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

TOPIC_NAME = 'persons'
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

# print("Connecting to Kafka server: " + KAFKA_SERVER)
print("Sending message Kafka topic: " + TOPIC_NAME)

# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

#from kafka import KafkaConsumer




consumer = KafkaConsumer(TOPIC_NAME,
                         group_id='person',
                         bootstrap_servers=KAFKA_SERVER)

for message in consumer:
    print (message)
    person_msg = message.value.decode('utf-8')
    print('{}'.format(person_msg))
    person = json.loads(person_msg)
    request_value = {
        "first_name": person["first_name"],
        "last_name": person["last_name"],
        "company_name": person["company_name"]
    }
    new_person: Person = PersonService.create(request_value)
    print(new_person)
    logging.info("new person")
    logging.info(new_person)
    print("Receive a message")

    # print(request_value)
    # logging.info(request_value)

    

# if __name__ == '__main__':



    # Read arguments and configurations and initialize
    # args = ccloud_lib.parse_args()
    # config_file = args.config_file
    # topic = args.topic
    # conf = ccloud_lib.read_ccloud_config(config_file)

    # Create Consumer instance
    # 'auto.offset.reset=earliest' to start reading from the beginning of the
    #   topic if no committed offsets exist
    # consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    # consumer_conf['group.id'] = 'python_example_group_1'
    # consumer_conf['auto.offset.reset'] = 'earliest'
    # consumer = KafkaConsumer(TOPIC_NAME, 
    #                         group_id='udaconnect',
    #                         bootstrap_servers=KAFKA_SERVER,
    #                         auto_offset_reset='earliest')

    # Subscribe to topic
    #consumer.subscribe([topic])

    # Process messages
    # total_count = 0
    # try:
    #     while True:
    #         msg = consumer.poll(1.0)
    #         if msg is None:
    #             # No message available within timeout.
    #             # Initial message consumption may take up to
    #             # `session.timeout.ms` for the consumer group to
    #             # rebalance and start consuming
    #             print("Waiting for message or event/error in poll()")
    #             continue
    #         elif msg.error():
    #             print('error: {}'.format(msg.error()))
    #         else:
    #             # Check for Kafka message
    #             record_key = msg.key()
    #             record_value = msg.value()
    #             data = json.loads(record_value)
    #             count = data['count']
    #             total_count += count
    #             print("Consumed record with key {} and value {}, \
    #                   and updated total count to {}"
    #                   .format(record_key, record_value, total_count))
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     # Leave group and commit final offsets
    #     consumer.close()

# def create_person(person_date):

#     kafka_data = json.dumps(person_data).encode()
#     print(kafka_data)

#     producer.send(TOPIC_NAME, kafka_data)


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





# def get_persons():



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



    # def Create(self, request, context):

    #     request_value = {
    #         "id": request.id,
    #         "first_name": request.first_name,
    #         "last_name": request.last_name,
    #         "company_name": request.company_name
    #     }
    #     print(request)
    #     new_person: Person = PersonService.create(request_value)
    #     # PersonService.create(new_person)
    #     print(new_person)
    #     logging.info("new person")
    #     logging.info(new_person)
    #     print("Receive a message")

    #     #request_value = PersonService.retrieve_all()
        
        
    #     print(request_value)
    #     logging.info(request_value)
    #     #result = person_pb2.PersonMessageList()
    #     #result.orders.extend(request_value)

    #     #return result
    #     return person_pb2.PersonMessage(**request_value)
