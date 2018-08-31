import logging

from flask import current_app
from flask_restful import Resource

from busy_wait import busy_wait_query

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class ExampleResource(Resource):

    def get(self):
        pl = busy_wait_query()
        LOGGER.info("Hello world")
        if len(pl) > 0:
            return str(pl[0].warehouse_id)
