import argparse
from confluent_kafka import KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

kafka_conf = {
    "bootstrap.servers": "localhost:9092",
}

admin_client = AdminClient(kafka_conf)


def print_topic_details(topic_name):
    try:
        topic_metadata = admin_client.list_topics(timeout=10).topics[topic_name]
        print(f"Topic Name: {topic_name}")
        print(f"Number of Partitions: {len(topic_metadata.partitions)}")
        for p in topic_metadata.partitions.values():
            print(
                f"  Partition: {p.id}, Leader: {p.leader}, Replicas: {p.replicas}, ISR: {p.isrs}"
            )
    except Exception as e:
        print(f"Error retrieving topic details: {e}")


def delete_topic(topic_name):
    try:
        fs = admin_client.delete_topics([topic_name])
        for _, f in fs.items():
            f.result()
        print(f"Topic '{topic_name}' deleted.")
    except KafkaError as e:
        print(f"Error deleting topic: {e}")


def create_topic(topic_name, num_partitions, replication_factor):
    try:
        topic = NewTopic(
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        fs = admin_client.create_topics([topic])
        for topic, f in fs.items():
            f.result()
        print(f"Topic '{topic_name}' created.")
    except KafkaError as e:
        print(f"Error creating topic: {e}")


def main():
    parser = argparse.ArgumentParser(description="Simple Kafka Topic Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for printing topic details
    parser_print = subparsers.add_parser("print", help="Print topic details")
    parser_print.add_argument("topic", type=str, help="Topic name to print details")

    # Subparser for deleting a topic
    parser_delete = subparsers.add_parser("delete", help="Delete a topic")
    parser_delete.add_argument("topic", type=str, help="Topic name to delete")

    # Subparser for creating a topic
    parser_create = subparsers.add_parser("create", help="Create a topic")
    parser_create.add_argument("topic", type=str, help="Topic name to create")
    parser_create.add_argument("partitions", type=int, help="Number of partitions")
    parser_create.add_argument("replication", type=int, help="Replication factor")

    args = parser.parse_args()

    if args.command == "print":
        print_topic_details(args.topic)
    elif args.command == "delete":
        delete_topic(args.topic)
    elif args.command == "create":
        create_topic(args.topic, args.partitions, args.replication)


if __name__ == "__main__":
    main()
