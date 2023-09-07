import os
from kafka import KafkaConsumer
import json
import datetime

from models import Location
from services import LocationService



TOPIC_NAME = 'location'
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

print("Sending message Kafka topic: " + TOPIC_NAME)



consumer = KafkaConsumer(TOPIC_NAME,
                         group_id='location',
                         bootstrap_servers=KAFKA_SERVER)

for message in consumer:
    print (message)
    location_msg = json.loads(message.value.decode('utf-8'))
    print('{}'.format(location_msg))
    #creation_time = datetime.datetime.utcnow()
    #location = json.loads(location_msg)
    location = {
        'person_id': location_msg["person_id"],
        'longitude': location_msg["longitude"],
        'latitude': location_msg["latitude"],
        #'creation_time': creation_time
    }
    print(location)
    new_location: Location = LocationService.create(location)
    print(new_location)

    # request_value = {
    #     "first_name": person["first_name"],
    #     "last_name": person["last_name"],
    #     "company_name": person["company_name"]
    # }
    # new_person: Person = PersonService.create(request_value)
    # print(new_person)
    # logging.info("new person")
    # logging.info(new_person)
    # print("Receive a message")

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