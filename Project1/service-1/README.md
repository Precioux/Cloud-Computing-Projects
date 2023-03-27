# HTTP Server

This is a Python application built with FastAPI that provides several endpoints for managing email submissions and job status checking. It interacts with a PostgreSQL database to store information about email submissions and job status, as well as an S3 bucket for file storage. The application also uses RabbitMQ for sending messages to other services.

The main endpoints include:

    - /up: A simple endpoint that returns a "Hey!" message to indicate that the application is up and running.
    - /submit_email: A POST endpoint that allows users to submit an email with a file attachment. The email information is stored in the database and the file is saved to S3.
    - /check_email: A GET endpoint that checks the status of an email submission based on its ID. If the submission is enabled, a message is sent to a RabbitMQ queue to start processing the submission.
    - /check_user: A GET endpoint that retrieves a list of job status objects associated with a given email address.

The application is started with Uvicorn and runs on port 8000.

## Requirements

You can install them by running the following command:

pip install -r requirements.txt
