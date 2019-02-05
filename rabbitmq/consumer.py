import pika
from incremental_dbscan import initiate_dbscan


connection = pika.BlockingConnection(pika.ConnectionParameters(
    '83.212.238.159'))
channel = connection.channel()

# Declare the channel on the specific queue
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    initiate_dbscan(body)


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
