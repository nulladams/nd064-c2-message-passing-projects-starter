import grpc
import location_pb2
import location_pb2_grpc

#from kafka import KafkaProducer
import json
from concurrent import futures
import time

TOPIC_NAME = "location"
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

def sendmsg(person_id, lon, lat):

    msg = {
        'person_id': person_id,
        'lon': lon,
        'lat': lat
    }

    print('sending message to kafka ')
    print(msg)

    producer.send(TOPIC_NAME, 
                  json.dumps(msg, indent=2).encode('utf-8')
    ).add_callback(on_send_success).add_errback(on_send_error)
    producer.flush()


class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Get(self, request, context):

        print("entrei")

        return location_pb2.Empty()

    def Create(self, request, context):

        print(request)

        request = {
            'person_id': request.person_id,
            'longitude': request.longitude,
            'latitude': request.latitude
        }

        # print('Processing request message' + request)
        # producer.send(TOPIC_NAME, json.dumps(
        #     request, indent=2).encode('utf-8'))

        #sendmsg(request.person_id, request.longitude, request.latitude)

        return location_pb2.LocationMessage(**request)

    



print("Connecting to Kafka server: " + KAFKA_SERVER)
print("Sending message Kafka topic: " + TOPIC_NAME)

#producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("oohh")
print('gRPC Server starting on port 5018')
server.add_insecure_port('[::]:5018')
server.start()
server.wait_for_termination()



