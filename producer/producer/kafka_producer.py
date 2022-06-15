"""Actual functionality to produce data to kafka topics"""
from asyncio.tasks import gather
from datetime import datetime
from functools import lru_cache
from logging import getLogger
from typing import List
from uuid import uuid4

from aiokafka import AIOKafkaProducer

from producer import producer_settings
from producer.model import Event, StreamEvent

_topic = producer_settings.topic
_broker = producer_settings.broker

logger = getLogger(__name__)


@lru_cache
async def get_aioproducer():
    """Get an aioproducer."""
    return AIOKafkaProducer(bootstrap_servers=_broker)


async def startup_event():
    """Start the kafka producer on start up"""
    await get_aioproducer().start()


async def shutdown_event():
    """Stop the kafka producer on shut down"""
    await get_aioproducer().stop()


async def send_events_to_topic(
    events: List[Event],
    unique_id: str,
    aioproducer: AIOKafkaProducer,
):
    """Add events to the main topic."""

    await gather(
        *[
            aioproducer.send(
                topic=_topic,
                value=StreamEvent(
                    event=event,
                    unique_id=int(unique_id),
                )
                .json()
                .encode("ascii"),
            )
            for event in events
        ]
    )


async def submit_events_to_topic(
    events: List[Event],
    aioproducer: AIOKafkaProducer,
):
    """
    Submit some events to the topic
    """
    logger.info("Starting event generation and submission", extra=producer_settings.dict())

    unique_id = uuid4()
    await send_events_to_topic(events, unique_id=unique_id, aioproducer=aioproducer)
    logger.info(
        "Submitted event to topic",
        extra={"id": unique_id, "timestamp": datetime.now(), "topic": {producer_settings.topic}},
    )
    return True
