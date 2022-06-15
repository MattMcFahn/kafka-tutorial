from dotenv import load_dotenv

from producer.config import get_settings

load_dotenv(".env")
producer_settings = get_settings()
