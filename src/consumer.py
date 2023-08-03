import pika

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Direct exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='direct')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Fanout exchange
channel.exchange_declare(exchange='fanout_logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='fanout_logs', queue=queue_name)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Topic exchange
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='topic.info')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Headers exchange
channel.exchange_declare(exchange='headers_logs', exchange_type='headers')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(
    exchange='headers_logs', 
    queue=queue_name, 
    arguments={'x-match': 'all', 'format': 'pdf', 'type': 'report'}
)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
