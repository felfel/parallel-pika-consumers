# -*- coding: utf-8 -*-

import logging
import pika
import time
from flask import Flask
import threading

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def create_app(config=None):
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # init app and config
    app = Flask(__name__)

    # configure flask to route urls with or without trailing slashes
    app.url_map.strict_slashes = False

    connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@127.0.0.1/"))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    def test(ch, method, body):
        print(" [x] Received %r" % (body,))
        t1 = time.time()
        time.sleep(2)
        # while 1:
        #     if t1 + 2 < time.time():
        #         break

        print('done')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback(ch, method, properties, body):
        gevent.spawn(test, ch, method, body)  # 协程启动，没有调用join，因为rabbitmq本身是阻塞的,可以不用join

    channel.basic_qos(prefetch_count=50)  # 并发的数量
    channel.basic_consume(callback, queue='hello')
    channel.start_consuming()
    # TODO: Stop consumer on exit gracefully (stop pika thread gracefully)

    return app


app = create_app()
