import pika

rabbitmq_ip = open('rabbitmq_ip', 'r')

connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_ip))
channel = connection.channel()

channel.queue_declare(queue='hello')
message="this is a test message"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

connection.close()
