from db.postgres import *
import asyncio
import uuid
import json
from fastapi import FastAPI, Body
from typing import List
from fastapi import FastAPI, Body
from typing import List
import requests
from api.mailgun import send_simple_message
import json
from tabulate import tabulate
import asyncio
import datetime
from api.s3 import *


def add_results(id, output):
    print(f'id = {id} output = {output}')
    now = datetime.datetime.now()
    execute_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current date and time as string:", execute_date)
    filelink = get_url(find_file(id))
    print(f'filelink : {filelink}')
    # insert to db results_table
    query_results = results_table.insert().values(upload=id, output=output, execute_date=execute_date,
                                                  filelink=filelink)
    with engine.connect() as conn:
        conn.execute(query_results)

    print('Added to result_table successfully')


def sendMail(id, status_id, result):
    uploads_data = json.loads(get_data_from_uploads_table(id))
    email = uploads_data['email']

    if status_id == 0:
        subject = f'Error while compiling code - {id}'
        status = 'Error'
        enable_off(id)

    elif status_id == 1:
        subject = f'Successful Code result - {id}'
        status = 'Success'
        status_executed(id)

    table_data = [['Response from codeX:', ''], [f'Status: {status}', '']]
    for key, value in result.items():
        table_data.append([f'{key}:', value])

    table = tabulate(table_data, tablefmt="plain")
    text = f'Hi,\n\nYour code request {status.lower()}ed!\n\n{table}\n\nRegards,\n\nPrecioux'
    send_simple_message(email, subject, text)
    print('Email sent successfully!')


def checkLang(lang_str):
    if lang_str == 'Java' or lang_str == 'java':
        return 'java'
    if lang_str == 'Python' or lang_str == 'python' or lang_str == 'Py' or lang_str == 'py':
        return 'py'
    if lang_str == 'C' or lang_str == 'c':
        return 'c'
    if lang_str == 'CPP' or lang_str == 'cpp' or lang_str == 'Cplusplus':
        return 'cpp'
    if lang_str == 'javascript' or lang_str == 'JS' or lang_str == 'JavaScript' or lang_str == 'js':
        return 'js'
    if lang_str == 'GO' or lang_str == 'go':
        return 'go'
    if lang_str == 'CS' or lang_str == 'cs':
        return 'cs'


def preRunner(job_list):
    for job in job_list:
        obj = job.get('job')
        code_obj = obj.get('job')
        print(f'obj : {obj}')
        code_data = json.loads(code_obj)
        language = checkLang(code_data['language'])
        url = "https://api.codex.jaagrav.in"
        payload = {
            "code": code_data['contents'],
            "language": language,
            "inputs": code_data['inputs']
        }
        headers = {"Authorization": "Bearer <access_token>"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f'Response : {result}')
            if result['status'] == 200:
                sendMail(obj['upload'], 1, result)
                add_results(obj['upload'], result['output'])
            else:
                sendMail(obj['upload'], 0, result)
        else:
            print(f"Error running job {job['id']}: {response.text}")


async def get_new_jobs():
    await database.connect()
    new_jobs = await get_none_executed_jobs()
    await database.disconnect()
    return new_jobs


async def main():
    job_list = []
    while True:
        new_jobs = await get_new_jobs()
        if new_jobs:
            for job in new_jobs:
                job_obj = json.loads(job)
                job_id = str(job_obj['id'])
                job_dict = {"id": job_id, "job": job_obj}
                if job_dict not in job_list:
                    job_list.append(job_dict)
                    print(f"Added job with ID {job_id} to the list")
            preRunner(job_list)
        else:
            print("No new jobs found, waiting...")
        await asyncio.sleep(60)  # Wait for 60 seconds before checking again


if __name__ == "__main__":
    asyncio.run(main())
