import logging
import os


class Config:
    DEBUG = os.environ.get("DEBUG", True)

    def configure_logger(name):
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name)
        return logger
