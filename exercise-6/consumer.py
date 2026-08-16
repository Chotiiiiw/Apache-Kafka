from confluent_kafka import Consumer

processed_events = set()

consumer = Consumer({
    "bootstrap.servers": "localhost:19092",
    "group.id": "idempotent-workers",
    "auto.offset.reset": "earliest",
})

consumer.subscribe(["idempotent-lab"])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    event_id = msg.value().decode("utf-8")

    if event_id in processed_events:
        print("SKIP duplicate:", event_id)
        continue

    print("PROCESS:", event_id)
    processed_events.add(event_id)