import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Direct exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
channel.basic_publish(exchange='direct_logs', routing_key='direct', body='Direct Hello World!')

# Fanout exchange
channel.exchange_declare(exchange='fanout_logs', exchange_type='fanout')
channel.basic_publish(exchange='fanout_logs', routing_key='', body='Fanout Hello World!')

# Topic exchange
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
channel.basic_publish(exchange='topic_logs', routing_key='topic.info', body='Topic Hello World!')

# Headers exchange
channel.exchange_declare(exchange='headers_logs', exchange_type='headers')
channel.basic_publish(
    exchange='headers_logs',
    routing_key='',
    body='Headers Hello World!',
    properties=pika.BasicProperties(headers={'x-match': 'all', 'format': 'pdf', 'type': 'report'})
)

print(" [x] Sent messages")
connection.close()
