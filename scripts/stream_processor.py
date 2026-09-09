'''
in this code, first we consume data from topic row_factor that ew create to produce data 
second produce processed data to silver layer through ommit all missing values row
finally send it to new topic called clean_event
'''
import json
from kafka import KafkaConsumer,KafkaProducer
BOOTSTRAP_SERVERS=['kafka:9092']
INPUT_TOPIC="row_factor"
OUTPUT_TOPIC='clean_event'
GROUP_ID="silver-stream-processor"

VALID_EVENTS_TYPE=["PAGE_VIEW", "ADD_TO_CART", "PURCHASE"]
consumer=KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

producer=KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    key_serializer=lambda k: k.encode('utf-8') if k else None,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def is_valid_event(event):
    if not event.get('customer_id'):
        return False
    if  event.get('event_type') not in VALID_EVENTS_TYPE:
        return False
    if event.get('amount') is None or event.get('amount')<=0:
        return False
    if not event.get('currency'):
        return False
    if event.get('is_valid') is not True:
        return False
    return True
print("Starting Silver Streaming processing")

for message in consumer:
    key=message.key
    event=message.value
    if is_valid_event(event):
        producer.send(
            topic=OUTPUT_TOPIC,
            key=key,
            value=event
        )
        print(f"FORWARDED | key={key} | event_type={event['event_type']}")
    else:
        print(f"DROPPED | key={key} | reason=invalid")
    consumer.commit()
