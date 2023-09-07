import json
import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc


def sendmsg(person_id, lat, lon):

    location = location_pb2.LocationMessage(
        person_id=person_id,
        latitude=lat,
        longitude=lon
    )

    response = stub.Create(location)


#channel = grpc.insecure_channel("grpc-location-server.default.svc.cluster.local:5022")
channel = grpc.insecure_channel("localhost:30022")
stub = location_pb2_grpc.TestServiceStub(channel)

stub = location_pb2_grpc.LocationServiceStub(channel)

sendmsg(6, "42.9435345", "-12.4234234")