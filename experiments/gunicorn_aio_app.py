# -*- coding: utf-8 -*-

import logging
import aio_pika
import asyncio
from flask import Flask
import threading

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


async def process_message(message: aio_pika.IncomingMessage):
    with message.process():
        print(message.body)
        print('gonna take a nap here...')
        await asyncio.sleep(1)
        print('done.')


async def pika(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )

    queue_name = "test_queue"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be
    # processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(
        queue_name, auto_delete=True
    )

    await queue.consume(process_message)


def run_pika():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pika(loop))
    loop.run_forever()


def create_app(config=None):
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # init app and config
    app = Flask(__name__)

    # configure flask to route urls with or without trailing slashes
    app.url_map.strict_slashes = False

    thread = threading.Thread(target=run_pika)
    thread.setDaemon(True)
    thread.start()

    # TODO: Stop consumer on exit gracefully (stop pika thread gracefully)

    return app


app = create_app()
