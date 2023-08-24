import time
import random

import pika


def callback(ch, method, properties, body):
    print('---')
    print(f'Start processing message {body=}, {ch=}, {method=}, {properties=}')

    time.sleep(x := random.randint(3, 8))

    ch.basic_ack(delivery_tag=method.delivery_tag)

    print(f'Message processed for {x} seconds {body=}')
    print('---')


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        channel.basic_qos(prefetch_count=1)

        # Direct exchange
        channel.basic_consume(queue='direct_queue', on_message_callback=callback, auto_ack=False)

        # Fanout exchange
        channel.basic_consume(queue='fanout_queue', on_message_callback=callback, auto_ack=False)

        # Topic exchange
        channel.basic_consume(queue='topic_queue', on_message_callback=callback, auto_ack=False)

        # Headers exchange
        channel.basic_consume(queue='headers_queue', on_message_callback=callback, auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f'Connection was closed, retrying... Error: {e}')
        time.sleep(5)

    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    print('Starting consumer')
    time.sleep(30)  # or wait-for-it script

    main()
