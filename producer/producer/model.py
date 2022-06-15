"""Pydantic base models to send to Kafka topic"""

from pydantic import BaseModel


class Event(BaseModel):
    """Event holding random numbers of different distributions"""

    random: float
    uniform: float
    triangular: float
    betavariate: float
    expovariate: float
    gammavariate: float
    gauss: float


class StreamEvent(BaseModel):
    """Stream event to be put on the Kafka topic"""

    unique_id: str
    event: Event
