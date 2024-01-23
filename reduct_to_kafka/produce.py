import asyncio
from time import time_ns
from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from reduct import Client, Bucket

client = Client("http://127.0.0.1:8383")

kafka_conf = {
    "bootstrap.servers": "localhost:9092",
}


def create_kafka_topic(
    topic_name, num_partitions, replication_factor, kafka_broker="localhost:9092"
):
    # Create an AdminClient object with the broker information
    admin_client = AdminClient({"bootstrap.servers": kafka_broker})

    # Check if the topic already exists
    current_topics = admin_client.list_topics(timeout=10).topics
    if topic_name in current_topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    # Define the new topic along with its partitions and replication factors
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )
    try:
        # Request the creation of the new topics on the server
        fs = admin_client.create_topics([topic])

        # Wait for each operation to finish.
        for topic, f in fs.items():
            f.result()

    except KafkaError as e:
        print(f"Failed to create Kafka topic: {e}")


async def writer():
    """Write data with toggling good flag."""
    bucket: Bucket = await client.create_bucket("bucket", exist_ok=True)
    good = True
    for _ in range(21):
        data = b"Some blob of data"
        ts = int(time_ns() / 10000)
        await bucket.write("entry-1", data, ts, labels=dict(good=good))
        print(f"Writer: Record written: ts={ts}, good={good}")
        good = not good
        await asyncio.sleep(1)


async def subscriber():
    """Subscribe to good records and publish them to Kafka."""
    producer = Producer(kafka_conf)
    bucket: Bucket = await client.create_bucket("bucket", exist_ok=True)
    counter = 0
    await asyncio.sleep(1)
    async for record in bucket.subscribe(
        "entry-1",
        start=int(time_ns() / 10000),
        poll_interval=0.2,
        include=dict(good=True),
    ):
        metadata = {"timestamp": record.timestamp, "good": record.labels.get("good")}
        print(f"Subscriber: Publishing to Kafka: {metadata}")
        producer.produce("metadata_topic", str(metadata).encode())
        counter += 1
        if counter == 10:
            break
    producer.flush()


async def main():
    create_kafka_topic("metadata_topic", num_partitions=1, replication_factor=1)
    await asyncio.gather(writer(), subscriber())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
