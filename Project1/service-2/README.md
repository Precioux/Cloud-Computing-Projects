# Job Executer

This code defines functions for receiving messages from a message queue, processing the message data, and inserting the result into a database. The create_json function creates a JSON object from input parameters, stringCreator reads a file's content and creates a JSON object, callback is called when a message is received from the message queue and processes the data, and main sets up the connection to the message queue and waits for messages. When a message is received, callback is called to process the message data and insert the result into the database.

The program uses the pika library to connect to a message queue, and the requests library to make HTTP requests. It also imports functions from two other modules, db.postgres and api.s3.

To run the program, run the main function. The program will wait for messages on a message queue, and process them when they arrive.
