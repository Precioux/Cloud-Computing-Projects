from db.postgres import *
import asyncio


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
            job_list.extend(new_jobs)
            print(f"Added {len(new_jobs)} new jobs to the list")
        else:
            print("No new jobs found, waiting...")
        await asyncio.sleep(60)  # Wait for 60 seconds before checking again


if __name__ == "__main__":
    asyncio.run(main())
