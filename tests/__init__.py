import os

from fastapi_server.constants import SETTINGS

SETTINGS.CONFIG = os.path.join(os.path.dirname(__file__), "test_data", "config.yaml")
