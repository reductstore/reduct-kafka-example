import asyncio
from reduct import Client, Bucket

client = Client("http://127.0.0.1:8383")


async def read_records(bucket_name, entry_name):
    bucket: Bucket = await client.create_bucket(bucket_name, exist_ok=True)

    async for record in bucket.query(entry_name):
        print("=" * 60)
        print(f"Record timestamp: {record.timestamp}")
        print(f"Record size: {record.size}")
        print(f"Metadata: {record.labels}")
        async for chunk in record.read(10):
            print(f"First 10 bytes of data: {chunk}")
            break


async def main():
    bucket_name = "kafka_bucket"
    entry_name = "entry-1"
    await read_records(bucket_name, entry_name)


if __name__ == "__main__":
    asyncio.run(main())
