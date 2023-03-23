import json
import os
import sys
import functools
import asyncio
import pika
import requests
from db.postgres import database, engine, metadata, jobs_table, uploads_table, get_data_from_db
from api.s3 import *

AMQP_URL = "amqps://oujymswf:es5s05JBydcj_gRGJhR_JmPbNgrGwNo9@woodpecker.rmq.cloudamqp.com/oujymswf"


def create_json(language, inputs, contents):
    data = {
        "language": language,
        "inputs": inputs,
        "contents": contents
    }
    json_data = json.dumps(data)
    return json_data


def stringCreator(data):
    filename = find_file(data["id"])
    if filename is not None:
        print(f"File Name : {filename}")
        fileData = get_file_content(filename)
        if fileData is not None:
            print(f'File Data: {fileData}')
            queryString = create_json(data['language'], data['inputs'], fileData)
            print(f'Query string: {queryString}')
            # insert to db jobs_table
            query = jobs_table.insert().values(upload=data['id'],
                                               job=queryString)
            database.execute(query=query)
            print('Added to jobs_table successfully')

        else:
            print('File Content is Empty')
    else:
        print(f"File with id {data['id']} not found!")


def main():
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='emails')

    def callback(ch, method, properties, body):
        print(" Emails Received %r" % body)
        gotten_id = str(body).split(".")[0].split("'")[1]
        data = json.loads(get_data_from_db(gotten_id))
        if data["enable"] == 0:
            print('sending to string creator..')
            stringCreator(data)

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
