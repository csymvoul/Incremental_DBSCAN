import pika
from incremental_dbscan import initiate_dbscan

rabbitmq_ip = open('rabbitmq_ip', 'r')


connection = pika.BlockingConnection(pika.ConnectionParameters(
    rabbitmq_ip.read()))
channel = connection.channel()

# Declare the channel on the specific queue
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    # initiate_dbscan(body)


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print("[x] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
