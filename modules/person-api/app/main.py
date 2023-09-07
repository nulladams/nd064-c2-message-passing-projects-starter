import grpc
import person_pb2
import person_pb2_grpc


print("Sending msg")

channel = grpc.insecure_channel("localhost:5005")
stub = person_pb2_grpc.PersonServiceStub(channel)

person = person_pb2.PersonMessage(
    id=8,
    first_name="Leonardo",
    last_name="Adams",
    company_name="success"
)

response = stub.Create(person)
print(response.last_name)