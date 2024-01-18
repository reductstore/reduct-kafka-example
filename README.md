# Kafka-ReductStore Simple Application

## Overview

This application demonstrates a simple setup for using Apache Kafka with ReductStore. The setup includes a Kafka producer (`produce.py`) that writes data with a toggling `good` flag to ReductStore and then publishes metadata to a Kafka topic. A Kafka consumer (`consume.py`) is used to read messages from this topic. The services are containerized using Docker and managed with Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your machine.

- Python environment (preferably with virtualenv or similar tool).

## Setup and Configuration

### 1. Docker Compose

The `docker-compose.yml` file contains the configuration for Zookeeper, Kafka, and ReductStore services.

To start these services, navigate to the directory containing `docker-compose.yml` and run:

```bash

docker compose up

```

This command will download the necessary Docker images and start the services.

### 2. Python Environment

It's recommended to use a Python virtual environment. To set up and activate a virtual environment:

```bash

python -m venv .venv

source .venv/bin/activate

```

### 3. Install Dependencies

Install the required Python packages using:

```bash

pip install -r requirements.txt

```

The `requirements.txt` file should contain:

```

confluent-kafka

reduct

```

### 4. Running the Producer and Consumer Scripts

#### Producer (`produce.py`):

The producer script creates a Kafka topic, writes data to ReductStore, and publishes metadata to the Kafka topic. To run the script:

```bash

python produce.py

```

This script will:

- Create a Kafka topic named `metadata_topic`.

- Write data to ReductStore and publish metadata to the Kafka topic.

#### Consumer (`consume.py`):

The consumer script reads messages from the Kafka topic `metadata_topic`. To run the script:

```bash

python consume.py

```

This script will continuously read messages from the `metadata_topic` and print them to the console.

## Troubleshooting

- Ensure Docker services are up and running.

- Check if Kafka and Zookeeper ports (`9092` and `2181` respectively) are correctly mapped and accessible.

- Make sure ReductStore is running and accessible on port `8383`.

- Validate that the Kafka topic is correctly created.

- Confirm network accessibility if running scripts outside Docker where Kafka is hosted.

## Conclusion

This application provides a basic framework for integrating Kafka with ReductStore. It can be extended or modified for more complex data processing and streaming requirements.