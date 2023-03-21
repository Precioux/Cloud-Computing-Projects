import pika, sys, os

AMQP_URL = "amqps://oujymswf:es5s05JBydcj_gRGJhR_JmPbNgrGwNo9@woodpecker.rmq.cloudamqp.com/oujymswf"

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
channel = connection.channel()