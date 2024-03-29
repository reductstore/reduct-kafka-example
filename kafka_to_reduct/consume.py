import asyncio
from confluent_kafka import Consumer, KafkaException
from reduct import Client, Bucket

kafka_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "datasink_demo",
    "auto.offset.reset": "earliest",
}

reduct_client = Client("http://127.0.0.1:8383")
kafka_consumer = Consumer(kafka_conf)


async def consume_and_store(topic_name, bucket_name):
    try:
        bucket: Bucket = await reduct_client.create_bucket(bucket_name, exist_ok=True)

        kafka_consumer.subscribe([topic_name])
        while True:
            # Polling for messages from Kafka with async support
            msg = kafka_consumer.poll(0)
            if msg is None:
                await asyncio.sleep(1)
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Extracting the metadata and data from the message
            headers = (
                {k: v.decode("utf-8") for k, v in msg.headers()}
                if msg.headers()
                else {}
            )
            data = msg.value()

            # Writing data to ReductStore asynchronously
            await bucket.write(topic_name, data, labels=headers)
            print(
                f"Stored binary data of size {len(data)} bytes with headers: {headers}"
            )
    finally:
        kafka_consumer.close()


async def main():
    await consume_and_store("entry-1", "kafka_bucket")


if __name__ == "__main__":
    asyncio.run(main())
