# Code Runner

This code runs an asynchronous FastAPI app that checks for new jobs in a database table, retrieves the jobs, and then processes them by compiling and running code. The code uses the Codex API to compile and run code, and results are stored in a PostgreSQL database. The code sends an email to the user with the result of the job, and also includes a table with the output. The code supports multiple languages, including Java, Python, C, C++, JavaScript, and Go.

The main functions in the code include:

    - add_results(): inserts the job results into the database
    - sendMail(): sends an email to the user with the result of the job and includes a table with the output
    - checkLang(): checks the language of the code and returns the corresponding language code
    - preRunner(): compiles and runs the code using the Codex API, and sends an email with the result
    - get_new_jobs(): retrieves new jobs from the database
    - main(): main function that continuously checks for new jobs and processes them

The code relies on several modules, including asyncio, uuid, json, requests, tabulate, and datetime. It also imports several functions from other modules, including the postgres module for interacting with the database and the s3 module for storing files.
