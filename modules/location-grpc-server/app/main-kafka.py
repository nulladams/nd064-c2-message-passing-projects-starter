from kafka import KafkaProducer
import json

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

    print('sending message ')
    print(msg)

    producer.send(TOPIC_NAME, 
                  json.dumps(msg, indent=2).encode('utf-8')
    ).add_callback(on_send_success).add_errback(on_send_error)
    producer.flush()



TOPIC_NAME = "location"
KAFKA_SERVER = "kafka.default.svc.cluster.local:9092"

print("Connecting to Kafka server: " + KAFKA_SERVER)
print("Sending message Kafka topic: " + TOPIC_NAME)

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

sendmsg(32, 41.90027193268211, -87.6565015438099)
sendmsg(32, 42.00027193268211, -87.7565015438099)
sendmsg(31, 41.90027193268211, -87.8565015438099)
sendmsg(33, 41.90027193268211, -87.9565015438099)
sendmsg(33, 42.90027193268211, -87.7565015438099)



