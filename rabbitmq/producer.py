import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('83.212.238.159'))
channel = connection.channel()

channel.queue_declare(queue='hello')
message="this is a test message"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

connection.close()
