# -*- coding: utf-8 -*-

import logging
from flask import Flask
from experiments.main_tornado import ExampleConsumer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def create_app(config=None):

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # init app and config
    app = Flask(__name__)

    # configure flask to route urls with or without trailing slashes
    app.url_map.strict_slashes = False

    # TODO: an environment variable should define the state dev/test/prod
    #    app.config.from_object(DevelopmentConfig)

    LOGGER.info('Starting Example Consumer...')
    example = ExampleConsumer('amqp://guest:guest@localhost:5672/%2F')
    example.run()
    LOGGER.info('Done.')

    # TODO: Stop consumer on exit
    # @app.before_first_request
    # def activate_job():
    #
    #     except KeyboardInterrupt:
    #         example.stop()

    return app


app = create_app()
