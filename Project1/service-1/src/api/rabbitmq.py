import pika, sys, os

AMQP_URL = "amqps://oujymswf:es5s05JBydcj_gRGJhR_JmPbNgrGwNo9@woodpecker.rmq.cloudamqp.com/oujymswf"

def send(id):
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='emails')

    channel.basic_publish(exchange='', routing_key='emails', body=str(id))
    print(f"INFO:     Sent {id} to RabbitMQ")
    connection.close()

