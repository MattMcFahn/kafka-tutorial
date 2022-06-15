"""Main entrypoint for the producer application"""
import asyncio
from logging import getLogger

from producer import producer_settings
from producer.generate import generate_random_event
from producer.kafka_producer import get_aioproducer, submit_events_to_topic
from producer.logging_helper import setup_logging

setup_logging()

logger = getLogger(__name__)


async def main():
    """Generate events, send to topic"""
    producer = await get_aioproducer()
    logger.info("Starting producer", extra=producer_settings.dict())
    await producer.start()
    logger.info("Producer started", extra=producer_settings.dict())

    try:
        # Run forever
        while True:
            events = [generate_random_event() for _ in range(11)]
            await submit_events_to_topic(events=events, aioproducer=producer)

    finally:
        logger.info("Stopping producer", extra=producer_settings.dict())
        await producer.stop()
        logger.info("Producer stopped", extra=producer_settings.dict())


asyncio.run(main())
