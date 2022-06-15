"""Generate some numbers from common random distributions"""
from logging import getLogger
from random import (
    betavariate,
    expovariate,
    gammavariate,
    gauss,
    random,
    triangular,
    uniform,
)

from producer.model import Event

logger = getLogger(__name__)


def generate_random_event():
    """Generates some numbers from random distros and returns as an event"""
    event = Event(
        random=random(),
        uniform=uniform(a=0, b=1),
        triangular=triangular(),
        betavariate=betavariate(alpha=1, beta=1),
        expovariate=expovariate(lambd=1),
        gammavariate=gammavariate(alpha=100, beta=1),
        gauss=gauss(mu=0, sigma=1),
    )
    return event
