from time import sleep
import pika

rabbitmq_ip = open('../rabbitmq/rabbitmq_ip', 'r')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip.read()))
channel = connection.channel()

channel.queue_declare(queue='hello')

with open('../data/test_file.csv') as fp:
    for line in fp:
        message = line
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=message)

        print('[*] Now published: ' + message)

        # Publish a row to RabbitMQ every 3 seconds
        sleep(3)

connection.close()
