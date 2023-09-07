# from kafka import KafkaProducer
import json
import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

#channel = grpc.insecure_channel("location-grpc-server.default.svc.cluster.local:5018")
channel = grpc.insecure_channel("localhost:30018")
stub = location_pb2_grpc.LocationServiceStub(channel)

def sendmsg(person_id, lat, lon):

    location = location_pb2.LocationMessage(
        person_id=person_id,
        latitude=lat,
        longitude=lon
    )

    response = stub.Create(location)
    print(response)

print("yuhh")
stub.Get(location_pb2.Empty())
print("passei")


sendmsg(36, 41.9, -87.7)
# sendmsg(37, 42.9, -86.6)

#https://realpython.com/python-microservices-grpc/


# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)

# def on_send_error(excp):
#     log.error('I am an errback', exc_info=excp)

# def sendmsg(person_id, lon, lat):

#     msg = {
#         'person_id': person_id,
#         'lon': lon,
#         'lat': lat
#     }

#     print('sending message ')
#     print(msg)

#     producer.send(TOPIC_NAME, 
#                   json.dumps(msg, indent=2).encode('utf-8')
#     ).add_callback(on_send_success).add_errback(on_send_error)
#     producer.flush()




# TOPIC_NAME = "location"
# KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

# print("Connecting to Kafka server: " + KAFKA_SERVER)
# print("Sending message Kafka topic: " + TOPIC_NAME)

# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# sendmsg(39, 41.90027193268211, -87.6565015438099)
# sendmsg(39, 42.10027193268211, -87.9565015438099)




