import json
import os
import sys
import functools
import asyncio
import pika
import requests
from db.postgres import database, engine, metadata, jobs_table, uploads_table, get_data_from_db
import aio_pika

AMQP_URL = "amqps://oujymswf:es5s05JBydcj_gRGJhR_JmPbNgrGwNo9@woodpecker.rmq.cloudamqp.com/oujymswf"

# def process_email(ch, method, properties, body):
#     email_data = json.loads(body)
#     email_id = email_data["id"]
#     email_address = email_data["address"]
#     email_inputs = email_data["inputs"]
#     email_language = email_data["language"]
#
#     # Find the corresponding upload data from the uploads_table
#     query = uploads_table.select().where(uploads_table.c.id == email_id)
#     upload = await database.fetch_one(query=query)
#
#     if not upload:
#         # If the email ID is not found in the uploads_table, we can just ignore it
#         print(f"Email ID {email_id} not found")
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#         return
#
#     # Generate the job data
#     job_query = f"file={email_address}&inputs={email_inputs}&language={email_language}"
#     job_data = {"upload": upload["id"], "job": job_query, "status": "none-executed"}
#
#     # Insert the job data into the jobs_table
#     query = jobs_table.insert().values(job_data)
#     await database.execute(query=query)
#
#     print(f"Job created for email ID {email_id}")
#     ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='emails')

    def callback(ch, method, properties, body):
        print(" Emails Received %r" % body)
        gotten_id = str(body).split(".")[0].split("'")[1]
        data = get_data_from_db(gotten_id)
        print(f'Data : {data}')

    channel.basic_consume(queue='emails', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
