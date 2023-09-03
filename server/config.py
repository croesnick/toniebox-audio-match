import os

class Config:
    DEBUG = os.environ.get("DEBUG", True)