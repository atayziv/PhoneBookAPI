import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_from_env(key: str, default_value: str) -> str:
    return str(os.getenv(key)) if key in os.environ else default_value


class SETTINGS:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG = get_from_env("CONFIG", os.path.join(ROOT_DIR, "config.yaml"))
    DATABASE_URL = os.getenv("DATABASE_URL")
    NAME = "PHONE BOOK API SERVER"
    VERSION = "0.1.0"
