import os
import base64
import requests
import logging
import threading

import contextlib

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base
from .entities import *

EMAILS_API_URL = os.environ['EMAILS_API_URL']


@contextlib.contextmanager
def obtener_session():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['AVATAR_DB_USER'],
        os.environ['AVATAR_DB_PASSWORD'],
        os.environ['AVATAR_DB_HOST'],
        os.environ['AVATAR_DB_PORT'],
        os.environ['AVATAR_DB_NAME']
    ), echo=False)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


from .AvatarModel import AvatarModel

__all__ = [
    'AvatarModel'
]
