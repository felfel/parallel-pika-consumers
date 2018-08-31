import pika
import time
import gevent
from gevent import monkey;monkey.patch_all()
connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@127.0.0.1/"))
channel = connection.channel()
channel.queue_declare(queue='hello')


def test(ch, method, body):
    print(" [x] Received %r" % (body,))
    t1 = time.time()
    while 1:
        if t1 + 2 < time.time():
            break

    print('done')
    ch.basic_ack(delivery_tag = method.delivery_tag)


def callback(ch, method, properties, body):
    gevent.spawn(test, ch, method, body) #协程启动，没有调用join，因为rabbitmq本身是阻塞的,可以不用join


channel.basic_qos(prefetch_count=50) #并发的数量
channel.basic_consume(callback, queue='hello')
channel.start_consuming()