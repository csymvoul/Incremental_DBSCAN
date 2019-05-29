import pika
from incremental_dbscan import IncrementalDBSCAN

dbscan = IncrementalDBSCAN()
batch = 0


def callback(ch, method, properties, body):
    # print("[x] Received %r" % body.decode())
    send_to_incremental_dbscan(body.decode())
    global batch
    batch += 1


def send_to_incremental_dbscan(message):
    dbscan.set_data(message)
    # This is going to be done only the first few times until the DBSCAN creates the first clusters.
    # The initial data will be used to feed the DBSCAN in order to create the first clusters and then
    # the Incremental DBSCAN will be used.
    if batch < 50:
        dbscan.batch_dbscan()
    if batch >= 50:
        dbscan.incremental_dbscan_()


rabbitmq_ip = open('rabbitmq_ip', 'r')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip.read()))
channel = connection.channel()
# Declare the channel on the specific queue
channel.queue_declare(queue='hello')
first_row = True
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
# print("[x] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()