# kafka-tutorial

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: pylint](https://img.shields.io/badge/%20linter-pylint-%231674b1?style=flat)](https://github.com/PyCQA/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commmit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

This repo acts as a demo project to set up an event streaming infrastructure in a local docker-compose environment, with
a (single) python producer and consumer application.

The intent of this is to demo Kafka's capabilities to a data-centric audience:
1) Expose a local environment with a Kafka broker & zookeeper set-up to enable experimentation of event producer and
consumer applications, whilst avoiding getting into the complexities of brokers
2) Give an intro to the internals of kafka platform components to deepen understanding whilst developing data production
 and consumption applications
3) Provide example code for event producer and consumer applications in python (which is where data engineers are more
 likely to work)

For a brief intro to Kafka and event streaming, check out the [introduction](./docs/INTRO.md) page.

## Overview of docs

* [An introduction to event streaming](./docs/INTRO.md)
* [An overview of python kafka libraries](./docs/PYTHON-KAFKA.md)
* [Interacting with kafka brokers and clusters](./docs/KAFKA-BROKERS.md)

TODO: Anything else ?

## Pre-requisites

* [Pyenv](https://github.com/pyenv/pyenv) with python >=3.9.5, for its flexible environment support
* [Poetry](https://python-poetry.org/) for packaging and dependency management
* [Docker desktop](https://www.docker.com/products/docker-desktop/) for a local development environment
  * In particular, so we can easily set up a Kafka broker and topic
* [Make](https://www.gnu.org/software/make/) for ease of command line tools
  * Not fully necessary

## Overview of core components in the repo

* [docker-compose.yml](./docker-compose.yml) uses images available on docker hub and built locally to bring up a local dev
env for an event streaming system
  * Images for a kafka broker and zookeeper come from Docker hub (so we need minimal work to set them up)
* [producer](./producer) contains code for a python-kafka producer application
  * Self-contained with a [Dockerfile](./producer/Dockerfile) to create a local docker image
* [consumer](./consumer) contains code for a python-kafka consumer application to subscribe to a topic and consume events
  * Self-contained with a [Dockerfile](./consumer/Dockerfile) to create a local docker image
* [dash-app](./dash-app) contains code to create a dash application to show some results
  * Self-contained with a [Dockerfile](./dash-app/Dockerfile) to create a local docker image

## Setup (first use)

In the root of the repo, run:
```bash
pre-commit install
```

Navigate to the `producer` folder and run:
```bash
make build
```

Navigate to the `consumer` folder and run:
```bash
make build
```

Navigate to the `dash-app` folder and run:
```bash
make build
```

This will package the applications as docker images on your local daemon, tagged as `producer` and `consumer` respectively.

Back in the root directory, run:

```bash
make up profile=microservices
```

TODO: Explain how this works / what's going on

TODO: Explanation of what gets brought up in the docker-compose network

TODO: Documentation endpoints exposed and kafdrop

When you are ready to bring down the network, run:

```bash
make down profile=microservices
```

**TODO:**
* Finish consumer code
* More images / diagrams for the repo
* Docs / tutorials
* Make producer and consumer git submodules
* Decide what will trigger kafka producer. Should it just send per minute or something simple?

**Maybe TODO / would be nice:**
* Artifactory in docker network and build pipeline to push there and streamline build process


## Helpful reading

* [Apache Kafka docs](https://kafka.apache.org/documentation/) should of course always be the go-to resource
* [Wurstmeister's kafka connectivity guide](https://github.com/wurstmeister/kafka-docker/wiki)


## Extra reading / other key technologies in the kafka ecosystem

### General
* [Kafka v. Kafka-streams v. Kafka-connect](https://www.tutorialworks.com/kafka-vs-streams-vs-connect/)

### Consumers
* [Kafka connect](https://docs.confluent.io/platform/current/connect/index.html#:~:text=Kafka%20Connect%20is%20a%20free,Kafka%20Connect%20for%20Confluent%20Platform.)

### Brokers
* [AWS Managed Kafka Service](https://aws.amazon.com/msk/)
