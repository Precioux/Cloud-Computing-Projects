import asyncio
import sqlalchemy
import databases
import json

DATABASE_URL = "postgresql://root:BBHzCFOv9TbK1T0z31987RRa@alfie.iran.liara.ir:31794/postgres"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

uploads_table = sqlalchemy.Table(
    "uploads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("inputs", sqlalchemy.String),
    sqlalchemy.Column("language", sqlalchemy.String),
    sqlalchemy.Column("enable", sqlalchemy.Integer)
)

job_table = sqlalchemy.Table(
    "job",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("upload", sqlalchemy.Integer, sqlalchemy.ForeignKey("uploads.id")),
    sqlalchemy.Column("job", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String, default="none-executed")
)
results_table = sqlalchemy.Table(
    "results",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("upload", sqlalchemy.Integer, sqlalchemy.ForeignKey("uploads.id")),
    sqlalchemy.Column("output", sqlalchemy.String, default="none"),
    sqlalchemy.Column("execute_date", sqlalchemy.String, default="none"),
    sqlalchemy.Column("filelink", sqlalchemy.String, default="none")
)

metadata.create_all(engine)


def get_data_from_uploads_table(id):
    try:
        with engine.connect() as conn:
            query = uploads_table.select().where(uploads_table.c.id == id)
            result = conn.execute(query)
            data = result.fetchone()
            if data:
                print(f"INFO: Got data from DB for {id}")
                return json.dumps(dict(data))
            else:
                print(f"INFO: No data found in DB for {id}")
                return None
    except Exception as e:
        print(f"ERROR: Failed to get data from DB for {id}")
        print(f"Error message: {e}")
        return None


async def get_none_executed_jobs():
    try:
        async with database:
            query = job_table.select().where(job_table.c.status == "none-executed")
            results = await database.fetch_all(query)
            return [json.dumps(dict(row)) for row in results]
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")


async def print_job_table():
    try:
        async with database:
            query = job_table.select()
            results = await database.fetch_all(query)
            for row in results:
                print(dict(row))
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")


async def print_uploads_table():
    try:
        async with database:
            query = uploads_table.select()
            results = await database.fetch_all(query)
            for row in results:
                print(dict(row))
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")


async def print_results_table():
    try:
        async with database:
            query = results_table.select()
            results = await database.fetch_all(query)
            for row in results:
                print(dict(row))
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")




def enable_off(id):
    with engine.connect() as conn:
        query = uploads_table.update().values(enable=0).where(uploads_table.c.id == id)
        conn.execute(query)
        print(f"INFO: Updated enable off for {id}")
    # Fetch the updated row from uploads_table
    with engine.connect() as conn:
        query = uploads_table.select().where(uploads_table.c.id == id)
        result = conn.execute(query)
        updated_row = result.fetchone()
        print(f"INFO: Updated row from uploads_table: {updated_row}")


def status_executed(id):
    with engine.connect() as conn:
        query = job_table.update().values(status="executed").where(job_table.c.upload == id)
        conn.execute(query)
        print(f"INFO: Updated status executed for {id}")
    # Fetch the updated row from job_table
    with engine.connect() as conn:
        query = job_table.select().where(job_table.c.upload == id)
        result = conn.execute(query)
        updated_row = result.fetchone()
        print(f"INFO: Updated row from job_table: {updated_row}")

def status_inprogress(id):
    with engine.connect() as conn:
        query = job_table.update().values(status="in progress").where(job_table.c.upload == id)
        conn.execute(query)
        print(f"INFO: Updated status executed for {id}")
    # Fetch the updated row from job_table
    with engine.connect() as conn:
        query = job_table.select().where(job_table.c.upload == id)
        result = conn.execute(query)
        updated_row = result.fetchone()
        print(f"INFO: Updated row from job_table: {updated_row}")


async def main():
    await database.connect()
    #await print_uploads_table()
    #await print_job_table()
    await print_results_table()
    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
