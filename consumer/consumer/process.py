"""Process events"""

from consumer.db.main_table import write_event
from consumer.db.utils import get_db_engine


async def process_event(event: dict) -> None:
    """Processes an event and writes to DB"""
    # TODO: Can do any other processing here: transformation, enrichment, etc
    write_event(engine=get_db_engine(), event=event)
