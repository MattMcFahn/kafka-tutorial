"""Load env vars into a pydantic base class"""

from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Relevant application settings exposed via classifier_settings
    https://pydantic-docs.helpmanual.io/usage/settings/
    """

    topic: str
    broker: Optional[str]


@lru_cache
def get_settings(**kwargs):
    return Settings(**kwargs)
