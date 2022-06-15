from dotenv import load_dotenv

from consumer.config import get_settings

load_dotenv(".env")
consumer_settings = get_settings()
