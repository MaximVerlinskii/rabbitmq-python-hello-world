import time
import pika


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        # Direct exchange
        channel.basic_consume(queue='direct_queue', on_message_callback=callback, auto_ack=True)

        # Fanout exchange
        channel.basic_consume(queue='fanout_queue', on_message_callback=callback, auto_ack=True)

        # Topic exchange
        channel.basic_consume(queue='topic_queue', on_message_callback=callback, auto_ack=True)

        # Headers exchange
        channel.basic_consume(queue='headers_queue', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection was closed, retrying... Error: {e}")
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    print('Starting consumer')
    time.sleep(70)  # or wait-for-it script

    main()
