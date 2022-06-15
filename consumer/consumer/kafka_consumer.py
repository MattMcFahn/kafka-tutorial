"""Actual functionality to consume data from kafka topics"""
import json
from functools import lru_cache
from logging import getLogger

from aiokafka import AIOKafkaConsumer

from consumer import consumer_settings

_topic = consumer_settings.topic
_broker = consumer_settings.broker

logger = getLogger(__name__)


def deserializer(byte_obj: bytes) -> dict:
    return json.loads(byte_obj)


@lru_cache
async def get_aioconsumer():
    """Set up a consumer subscribed to the topic, and pass events down to processing"""
    consumer = AIOKafkaConsumer(
        _topic,
        bootstrap_servers=_broker,
        group_id="some_group",  # Consumer must be in a group to commit
        value_deserializer=deserializer,
        enable_auto_commit=True,  # Is True by default anyway
        auto_commit_interval_ms=1000,  # Autocommit every second
        auto_offset_reset="earliest",  # If committed offset not found, start
        # from beginning
    )
    return consumer
