from confluent_kafka import Consumer, KafkaException


def consume_messages(topic_name, kafka_broker="localhost:9092"):
    conf = {
        "bootstrap.servers": kafka_broker,
        "group.id": "mygroup",
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(conf)

    try:
        consumer.subscribe([topic_name])

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break
            print(f"Received message: {msg.value().decode('utf-8')}")
    finally:
        consumer.close()


consume_messages("metadata_topic")
