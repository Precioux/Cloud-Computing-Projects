## Cloud Computing Projects

This repository contains three projects related to cloud computing. Each project focuses on different aspects of cloud services and technologies. Here's an overview of each project:

### Project 1: Execution Service Implementation
In this project, you are required to implement an execution service. The main objective is to familiarize yourself with cloud services. You will utilize various cloud services for tasks such as creating a database, storing files, executing tasks, and sending emails.

In the execution service, each task is defined as a file that needs to be executed, and the result should be returned to the user. Users can upload one or multiple files containing Python, C, C++, Java, or other code onto the server and execute them. Finally, the execution result should be sent to the user as an email. If a user's file contains errors, the execution should be prevented, and an email alert should be sent to the user. It should also be ensured that each user can only execute files they have created.

For this project, you can utilize Liara Database for creating the database, Parsget Object Storage for file storage, RabbitMQ for task execution, and Mailgun for email services.

### Project 2: Docker and Kubernetes Deployment
The objective of this project is to work with Docker and Kubernetes. You will create a simple project using Docker and then deploy it on a Kubernetes server.

#### Step 1:
Start by creating an account on Docker Hub. Docker Hub is a powerful tool for managing and distributing Docker images. You can use cURL to upload your Docker image to Docker Hub. It is recommended to base your Docker image on a Linux distribution (preferably Alpine). Make sure your Docker image has cURL installed.

#### Step 2:
URL shortening is a widely used technique in modern web applications. It provides benefits such as making URLs more readable, reducing the number of characters in a URL, and enabling link tracking and analysis for business development. In this step, you will utilize a URL shortening API to develop a URL shortener service. Choose an API that does not require an API key or use one of the suggested APIs mentioned below:

- API Layer
- Bitly
- TinyURL

#### Step 3:
In this step, you will work with Minikube, which is a tool for easily running Kubernetes clusters. Set up Minikube on your system and bring up a Kubernetes cluster quickly.

### Project 3: MapReduce on Hadoop Cluster
The goal of this project is to execute MapReduce on a Hadoop cluster.

#### Step 1: Cluster Setup
Set up a Hadoop cluster. Write a MapReduce program that calculates the number of likes, retweets, and sources used for tweets related to Joe Biden, Donald Trump, and both candidates. Each line of output should contain the candidate name, the number of likes, the total number of retweets, and the program should calculate the total for each candidate. The output should indicate which portion of the tweets for each state falls between 9 am and 5 pm and also mention the total number of tweets for that state within the specified time interval.

#### Step 2: MapReduce Program Development and Execution
Develop and execute a MapReduce program similar to the one written in Step 1. However, this time, instead of determining the state from which the tweet was sent, use the latitude and longitude coordinates. The source field (Web App, iPhone, or Android) should be included in the output.

#### Step 3: Dataset Description
Provide detailed information about the dataset used for the MapReduce program.

Please note that the instructions provided here are a summary of the projects. It is recommended to refer to the actual project files in the repository for more detailed instructions, code samples, and additional resources.