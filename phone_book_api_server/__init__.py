import os

from phone_book_api_server.constants import SETTINGS

__all__ = ("SETTINGS",)

os.chdir(SETTINGS.ROOT_DIR)
