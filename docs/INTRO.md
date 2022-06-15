# An intro to event streaming & Kafka

I couldn't give a better high level overview of event streaming than the following excerpt from
[Apache Kafka's website](https://kafka.apache.org/documentation/):

> Event streaming is the digital equivalent of the human body's central nervous system. It is the technological foundation for the 'always-on' world where businesses are increasingly software-defined and automated, and where the user of software is more software.
>
> Technically speaking, event streaming is the practice of capturing data in real-time from event sources like databases, sensors, mobile devices, cloud services, and software applications in the form of streams of events; storing these event streams durably for later retrieval; manipulating, processing, and reacting to the event streams in real-time as well as retrospectively; and routing the event streams to different destination technologies as needed. Event streaming thus ensures a continuous flow and interpretation of data so that the right information is at the right place, at the right time.

Kafka is a particularly popular platform for event streaming.

For those familiar with distributed systems, event streaming may seem similar to
an implementation of a [simple queue service (`SQS`)](https://aws.amazon.com/sqs/).

Understanding the differences between a queue and an event streaming architecture is a useful exercise in teasing out
the use-case of Kafka.

## Why use event streaming? Why not a SQS?

Some key differences between an SQS and an event-streaming system are:
1) Queues can only deliver messages to one consumer. Multiple consumers can consume messages from a streaming broker.
2) Queues will lose messages forever once they are delivered. A streaming broker uses [distributed logging](https://dzone.com/articles/distributed-logging-architecture-for-microservices) to enable consumers to re-process messages.

Given this, Kafka is often implemented in distributed systems and microservices needing:
* Multiple applications / computers to consume from a single source of truth in a data-centric environment
* Real-time interactions
* [Polyglot persistence](https://en.wikipedia.org/wiki/Polyglot_persistence)
* Storing events for as long as desired as a single-source of truth

With this, it's time to look in more detail at the typical architecture of Kafka.

## Kafka components and architecture

![Kafka components](../images/Kafka%20components.drawio.png)
_Note - In the above diagram, the arrow for controlling consumer offsets does not always point to zookeeper in all flavours & versions of Kafka._
_E.g., for Kafka >= 0.9, offsets can be commited to the brokers instead in a special `__consumer_offsets` topic, and this may depend on how a consumer is configured as well._


Some key concepts in the internals of a Kafka server are:
* **Brokers** are the actual storage layer of data
* **Events** are single units of data stored in a broker. They record the fact that "something happened" in the real-world/your
business, and record metadata about that particular event.
  * Conceptually, an events has a `key`, `value`, `timestamp`, and optional metadata headers.
* **Topics** are similar to folders in a filesystem, with a broker consisting of multiple topics.
* Topics are **partitioned**, effectively meaning the events (messages/files) on a topic are spread over a number of
buckets on different brokers.
  * The importance of this is for scalability, allowing multiple applications to read/write to brokers & topics whilst
  retaining high throughput
* **Producers** are applications that will write events to topic(s)
* **Consumers** are applications that subscribe to (read & process) events from topics

**An example:** Say you have an e-commerce website selling wine. You may set up multiple topics to store and consume data
for:
* Sales
* Inventory
* Delivery
* Customers

Kafka producers may be set up to write events when a sale occurs via a website or app.

Such an event may look something like:
* `key: 1`
* ```value: {'customer':'Joe Bloggs', 'items':['Value Merlot', ...], ...}```
* `timestamp: 2022-01-01 T12:00:00`
* `headers: []`

You may set up a consumer application to inform warehouse operations based on these sales. Similarly, you could have a
producer to update inventory records based on deliveries. You may similarly have consumers supporting real time analytics
for management and reporting purposes.
