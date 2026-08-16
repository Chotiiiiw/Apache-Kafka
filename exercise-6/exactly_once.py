from confluent_kafka import Consumer, Producer, TopicPartition

consumer = Consumer({
    "bootstrap.servers": "localhost:19092",
    "group.id": "eos-workers",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

producer = Producer({
    "bootstrap.servers": "localhost:19092",
    "transactional.id": "eos-processor-1",
})

consumer.subscribe(["eos-input"])

producer.init_transactions()

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(msg.error())
        continue

    value = msg.value().decode("utf-8")

    producer.begin_transaction()

    try:
        output = f"processed-{value}"

        producer.produce(
            "eos-output",
            value=output
        )

        offsets = [
            TopicPartition(
                msg.topic(),
                msg.partition(),
                msg.offset() + 1
            )
        ]

        producer.send_offsets_to_transaction(
            offsets,
            consumer.consumer_group_metadata()
        )

        producer.commit_transaction()

        print("COMMITTED:", output)

    except Exception as e:
        producer.abort_transaction()
        print("ABORTED:", e)