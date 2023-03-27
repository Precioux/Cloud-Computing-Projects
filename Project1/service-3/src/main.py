from db.postgres import *
import asyncio
import uuid
import json
from fastapi import FastAPI, Body
from typing import List
from fastapi import FastAPI, Body
from typing import List
import requests


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
        # print(type(code_obj))
        # print(code_obj)
        code_data = json.loads(code_obj)
        # print(type(code_data))
        print(code_data)
        language = checkLang(code_data['language'])
        url = "https://api.codex.jaagrav.in"
        payload = {
            "code": code_data['contents'],
            "language": language,
            "inputs": code_data['inputs']
        }
        print(type(payload))
        headers = {"Authorization": "Bearer <access_token>"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f'Response : {result}')
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
                print(job)
                job_id = str(job_obj['id'])
                job_dict = {"id": job_id, "job": job_obj}
                if job_dict not in job_list:
                    job_list.append(job_dict)
                    print(f"Added job with ID {job_id} to the list")
                    # print(f'job dict : {job_dict}')
            preRunner(job_list)
        else:
            print("No new jobs found, waiting...")
        await asyncio.sleep(60)  # Wait for 60 seconds before checking again


if __name__ == "__main__":
    asyncio.run(main())
