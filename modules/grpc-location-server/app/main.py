import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer
import json
from concurrent import futures
import time

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

def sendmsg(person_id, longitude, latitude):

    msg = {
        'person_id': person_id,
        'longitude': longitude,
        'latitude': latitude
    }

    print('sending message to kafka ')
    print(msg)

    producer.send(TOPIC_NAME,
                  json.dumps(msg, indent=2).encode('utf-8')
    ).add_callback(on_send_success).add_errback(on_send_error)
    producer.flush()


class TestServicer(location_pb2_grpc.TestServiceServicer):

    def Get(self, request, context):

        print("entrei")
        print(request)

        msg = {
            'test': "oiee"
        }

        return location_pb2.TestMessage(**msg)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Get(self, request, context):

        print("entrei empty get ")

        return location_pb2.Empty()

    def Create(self, request, context):

        print("entrei Create")
        print(request)

        request = {
            'person_id': request.person_id,
            'longitude': request.longitude,
            'latitude': request.latitude
        }

        print('Processing request message')
        # producer.send(TOPIC_NAME, json.dumps(
        #     request, indent=2).encode('utf-8'))

        sendmsg(**request)

        return location_pb2.LocationMessage(**request)


TOPIC_NAME = "location"
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_TestServiceServicer_to_server(TestServicer(), server)
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("oohh")
print('gRPC Server starting on port 5022')
server.add_insecure_port('[::]:5022')
server.start()
server.wait_for_termination()