import grpc
import test_pb2
import test_pb2_grpc

import json
from concurrent import futures
import time

class TestServicer(test_pb2_grpc.TestServiceServicer):

    def Get(self, request, context):

        print("entrei")
        print(request)

        msg = {
            'test': "oiee"
        }

        return test_pb2.TestMessage(**msg)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
test_pb2_grpc.add_TestServiceServicer_to_server(TestServicer(), server)

print("oohh")
print('gRPC Server starting on port 5021')
server.add_insecure_port('[::]:5021')
server.start()
server.wait_for_termination()