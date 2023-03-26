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

metadata.create_all(engine)


def get_data_from_db(id):
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


async def print_job_table():
    try:
        async with database:
            query = job_table.select()
            results = await database.fetch_all(query)
            print(results)
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")

async def print_uploads_table():
    try:
        async with database:
            query = uploads_table.select()
            results = await database.fetch_all(query)
            print(results)
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")


async def main():
    await database.connect()
    await print_job_table()
    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
