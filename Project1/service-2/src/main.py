import json
import pika
from db.postgres import database, engine, metadata, jobs_table, uploads_table

def process_email(ch, method, properties, body):
    email_data = json.loads(body)
    email_id = email_data["id"]
    email_address = email_data["address"]
    email_inputs = email_data["inputs"]
    email_language = email_data["language"]

    # Find the corresponding upload data from the uploads_table
    query = uploads_table.select().where(uploads_table.c.id == email_id)
    upload = await database.fetch_one(query=query)

    if not upload:
        # If the email ID is not found in the uploads_table, we can just ignore it
        print(f"Email ID {email_id} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Generate the job data
    job_query = f"file={email_address}&inputs={email_inputs}&language={email_language}"
    job_data = {"upload": upload["id"], "job": job_query, "status": "none-executed"}

    # Insert the job data into the jobs_table
    query = jobs_table.insert().values(job_data)
    await database.execute(query=query)

    print(f"Job created for email ID {email_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up the RabbitMQ connection
credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(host="localhost", credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Set up the queue and bind it to the exchange
channel.exchange_declare(exchange="emails", exchange_type="direct")
result = channel.queue_declare(queue="jobs_queue", durable=True)
queue_name = result.method.queue
channel.queue_bind(exchange="emails", queue=queue_name, routing_key="jobs")

# Start consuming messages
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=process_email)
channel.start_consuming()

