import logging
import random
import time

from flask import current_app

from extensions import db
from product_locks import ProductLock

LOGGER = logging.getLogger(__name__)


def busy_wait_query():
    random_wait = 5  # random.randint(1, 50) / 10
    start_time = time.time()
    while start_time + random_wait > time.time():
        pass

    LOGGER.info("Hello world")
    pl = ProductLock.query.all()

    return pl
