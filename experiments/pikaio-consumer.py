import asyncio
import aio_pika


async def process_message(message: aio_pika.IncomingMessage):
    with message.process():
        print(message.body)
        print('gonna take a nap here...')
        await asyncio.sleep(1)
        print('done.')


async def main(loop):
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()