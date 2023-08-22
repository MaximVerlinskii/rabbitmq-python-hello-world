import pika
import time


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Direct exchange
    channel.exchange_declare(exchange='direct_test', exchange_type='direct')
    result = channel.queue_declare(queue='direct_queue')
    queue_name = result.method.queue
    channel.queue_bind(exchange='direct_test', queue=queue_name, routing_key='direct')

    # Fanout exchange
    channel.exchange_declare(exchange='fanout_test', exchange_type='fanout')
    result = channel.queue_declare(queue='fanout_queue')
    queue_name = result.method.queue
    channel.queue_bind(exchange='fanout_test', queue=queue_name)

    # Topic exchange
    channel.exchange_declare(exchange='topic_test', exchange_type='topic')
    result = channel.queue_declare(queue='topic_queue')
    queue_name = result.method.queue
    channel.queue_bind(exchange='topic_test', queue=queue_name, routing_key='topic.info')

    # Headers exchange
    channel.exchange_declare(exchange='headers_test', exchange_type='headers')
    result = channel.queue_declare(queue='headers_queue')
    queue_name = result.method.queue
    channel.queue_bind(
        exchange='headers_test',
        queue=queue_name,
        arguments={'x-match': 'all', 'format': 'pdf', 'type': 'report'}
    )
    connection.close()

    message_count = 0


    while True:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        message_count += 1
        message = f'Message {message_count}'

        channel.basic_publish(exchange='direct_test', routing_key='direct', body=message)
        channel.basic_publish(exchange='fanout_test', routing_key='', body=message)
        channel.basic_publish(exchange='topic_test', routing_key='topic.info', body=message)
        channel.basic_publish(
            exchange='headers_test',
            routing_key='',
            body=message,
            properties=pika.BasicProperties(headers={'x-match': 'all', 'format': 'pdf', 'type': 'report'})
        )

        print(f" [x] Sent {message}")
        connection.close()
        time.sleep(5)  # wait for 5 seconds before sending the next message


if __name__ == '__main__':
    print('Starting producer')
    time.sleep(50)  # or wait-for-it script

    main()
