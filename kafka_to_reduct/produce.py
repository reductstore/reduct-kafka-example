import asyncio
import os
import random
from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

kafka_conf = {
    "bootstrap.servers": "localhost:9092",
}

kafka_producer = Producer(kafka_conf)
kafka_admin_client = AdminClient(kafka_conf)


def create_kafka_topic(topic_name, num_partitions, replication_factor):
    current_topics = kafka_admin_client.list_topics(timeout=10).topics
    if topic_name in current_topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )
    try:
        fs = kafka_admin_client.create_topics([topic])
        for topic, f in fs.items():
            f.result()
    except KafkaError as e:
        print(f"Failed to create Kafka topic: {e}")


def generate_random_data(size_in_kb=1):
    return os.urandom(size_in_kb * 1024)


def callback(err, msg):
    if err is not None:
        print(f"Failed to deliver message to {msg.topic()}")
    else:
        print(f"Message {msg.topic()} sent to partition {msg.partition()}")


async def produce_binary_data(topic_name, num_messages=10):
    for _ in range(num_messages):
        data = generate_random_data(size_in_kb=random.randint(1, 900))
        metadata = {"size": str(len(data)), "type": "binary"}
        headers = [(key, value.encode("utf-8")) for key, value in metadata.items()]
        kafka_producer.produce(
            topic_name, value=data, headers=headers, callback=callback
        )
        kafka_producer.poll(0)
        await asyncio.sleep(1)
    kafka_producer.flush()


async def main():
    topic_name = "entry-1"
    create_kafka_topic(topic_name, num_partitions=4, replication_factor=1)
    await produce_binary_data(topic_name)


if __name__ == "__main__":
    asyncio.run(main())
