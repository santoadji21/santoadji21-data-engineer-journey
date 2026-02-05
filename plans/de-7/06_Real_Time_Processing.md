# Module 6: Real-Time Data & Event Streaming

## 🎯 Learning Objectives
* **Grasp** the Pub/Sub model vs. Message Queues.
* **Understand** Kafka Architecture: Topics, Partitions, Offsets, Consumer Groups.
* **Implement** a Python Producer and Consumer.

## 1. Why Real-Time?
Batch processing (Module 2) is like receiving a newspaper the next morning. Streaming is like reading a Twitter feed.
* **Use Cases:** Fraud detection (stop the card swipe *now*), Uber geolocations, Server monitoring.

## 2. Apache Kafka Core Concepts
* **Topic:** A log of events (immutable).
* **Partition:** A topic is sliced into partitions to allow parallel processing.
* **Offset:** The ID of a message. Kafka doesn't delete messages when read; it just remembers your "Offset" (bookmark).
* **Consumer Group:** Critical concept. If you have a group of 3 consumers reading a topic with 3 partitions, Kafka assigns one partition to each. This allows massive scale.

## 🧪 Hands-On Activity: Kafka in Python
**Goal:** Simulate a stream of sensor data.

**Step 1: Environment**
Ensure your Docker setup includes Zookeeper and Kafka (use Cursor to generate the `docker-compose` if needed).

**Step 2: Producer Script (`producer.py`)**
Use Cursor (`Cmd+K`) to write this:
"Write a Python script using `kafka-python`. It should act as a Producer. It generates a random temperature reading (20-30 degrees) every second and sends it to the topic 'sensors' as JSON."

**Step 3: Consumer Script (`consumer.py`)**
Use Cursor (`Cmd+K`):
"Write a Python Consumer script for the 'sensors' topic. It should read messages and print an alert if the temperature > 28 degrees."

**Step 4: Run Both**
Open two terminals in Cursor. Run `python producer.py` in one and `python consumer.py` in the other. Watch the real-time interaction.