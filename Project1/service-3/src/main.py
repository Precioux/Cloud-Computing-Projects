from db.postgres import *
import asyncio
import uuid
import json


async def get_new_jobs():
    await database.connect()
    new_jobs = await get_none_executed_jobs()
    await database.disconnect()
    return new_jobs

def preRunner(job_list):
    for job in job_list:


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
            preRunner(job_list)
        else:
            print("No new jobs found, waiting...")
        await asyncio.sleep(60)  # Wait for 60 seconds before checking again


if __name__ == "__main__":
    asyncio.run(main())
