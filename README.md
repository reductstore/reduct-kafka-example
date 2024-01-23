# Kafka-ReductStore Simple Demonstrations

## Overview

This collection features two simple demos that illustrate the integration of Apache Kafka with ReductStore in distinct ways. 

A simple Kafka Topic Management CLI tool (`kafka_cli.py`) is also included to facilitate the creation, listing, and deletion of Kafka topics.

### 1. Kafka to ReductStore Demo (kafka_to_reduct)

This demo shows how data can be streamed from Kafka to ReductStore. It includes a Kafka producer that writes binary data to a Kafka topic, and a Kafka consumer that reads from this topic and writes to ReductStore.

### 2. ReductStore to Kafka Demo (reduct_to_kafka)

In this setup, a Kafka producer writes data with a toggling `good` flag to ReductStore and then publishes metadata to a Kafka topic. A Kafka consumer script reads messages from this topic and prints the result.

### 3. Kafka CLI Tool (kafka_cli.py)

This simple command-line interface tool provides functionalities for creating, deleting, and printing details of topics.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Python environment (preferably with virtualenv).

## Setup and Configuration

### Docker Compose

Common `docker-compose.yml` configuration for Zookeeper, Kafka, and ReductStore. 

Start the services in detache mode with:

```bash
docker compose up -d
```

Logs can be viewed with:

```bash
docker compose logs -f
```

### Python Environment

Set up and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Dependencies include `confluent-kafka` and `reduct`.

### Running the Demos

#### Kafka to ReductStore (`kafka_to_reduct` folder):

- Producer (`produce.py`): Writes binary data to Kafka topic `entry-1`.

```bash
python kafka_to_reduct/produce.py
```

- Consumer (`consume.py`): Reads from Kafka topic `entry-1` and writes to ReductStore.

```bash
python kafka_to_reduct/consume.py
```

- Read (`read.py`): Reads from ReductStore bucket.

```bash
python kafka_to_reduct/read.py
```

#### ReductStore to Kafka (`reduct_to_kafka` folder):

- Producer (`produce.py`): Writes data to ReductStore and publishes metadata to Kafka.

```bash
python reduct_to_kafka/produce.py
```

- Consumer (`consume.py`): Reads and print from Kafka topic `metadata_topic`.

```bash
python reduct_to_kafka/consume.py
```

### Kafka CLI Tool Usage

- Print Topic Details:

    ```bash
    python kafka_cli.py print <topic_name>
    ```

    Replace `<topic_name>` with the name of the Kafka topic you want details for.

- Delete a Topic:

    ```bash
    python kafka_cli.py delete <topic_name>
    ```

    Replace `<topic_name>` with the name of the Kafka topic you wish to delete.

- Create a Topic:

    ```bash
    python kafka_cli.py create <topic_name> <num_partitions> <replication_factor>
    ```

    Replace `<topic_name>`, `<num_partitions>`, and `<replication_factor>` with your desired values.

## Troubleshooting

- Ensure Docker services are running

  - Tips: use `docker compose ps`

- Check Kafka and Zookeeper ports (`9092`, `2181`)

  - Tips: use `netstat`

- Ensure ReductStore is running on port `8383` 

  - Tips: open `http://localhost:8383` in your browser.

- Verify Kafka topic creation 

  - Tips: use CLI `python kafka_cli.py print <topic_name>`.

## Conclusion

This application provides a basic framework for integrating Kafka with ReductStore. It can be extended or modified for more complex data processing and streaming requirements.

If you have any questions or feedback, please contact us on [Discord](https://discord.com/invite/BWrCncF5EP).