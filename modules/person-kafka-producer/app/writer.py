import grpc
import person_pb2
import person_pb2_grpc


print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30015")
# channel = grpc.insecure_channel("localhost:5005")
stub = person_pb2_grpc.PersonServiceStub(channel)

person = person_pb2.PersonMessage(
    id=33,
    first_name="kai",
    last_name="waehner",
    company_name="confluent"
)

response = stub.Create(person)

print(response)

response = stub.Get(person_pb2.Empty())

print(response)