import json
import time
from concurrent import futures

import grpc
import test_pb2
import test_pb2_grpc
#channel = grpc.insecure_channel("test-server.default.svc.cluster.local:5021")
channel = grpc.insecure_channel("localhost:30015")
stub = test_pb2_grpc.TestServiceStub(channel)


print("yuhh")
resposta = stub.Get(test_pb2.TestMessage(test="success"))
print("passei")
print(resposta)