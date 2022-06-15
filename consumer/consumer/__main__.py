"""Main entrypoint for the consumer application"""
import asyncio
from logging import getLogger

from sqlalchemy.schema import CreateSchema

from consumer import consumer_settings
from consumer.db.main_table import metadata
from consumer.db.utils import get_db_engine
from consumer.kafka_consumer import get_aioconsumer
from consumer.logging_helper import setup_logging
from consumer.process import process_event

setup_logging()

logger = getLogger(__name__)


async def main():
    """Subscribe to topic and start listening, write to DB"""
    # Initialise DB engine and create
    logger.info("Setting up database")

    # TODO: Should just be part of a DB setup module
    engine = get_db_engine()
    if not engine.dialect.has_schema(engine, "main"):
        engine.execute(CreateSchema("main"))
    metadata.create_all(engine)
    logger.info("DB configured")

    logger.info("Starting kafka consumer", extra=consumer_settings.dict())
    consumer = await get_aioconsumer()
    logger.info("Kafka consumer started", extra=consumer_settings.dict())
    await consumer.start()
    async for message in consumer:  # Will periodically commit returned messages.
        logger.info("Read message", extra=consumer_settings.dict())
        event_content = message.value["event"]
        event_content["id"] = message.offset

        await process_event(event_content)
        logger.info("Message written to database", extra={**consumer_settings.dict(), **event_content})

        # try:
        #     logger.info("Read message", extra=consumer_settings.dict())
        #     event_content = message.value['event']
        #     await process_event(message.value)
        #     logger.info("Message written to database", extra=consumer_settings.dict())
        # except Exception as err:
        #     logger.error("Exception occurred", extra={"traceback": err})

    await consumer.stop()


asyncio.run(main())
