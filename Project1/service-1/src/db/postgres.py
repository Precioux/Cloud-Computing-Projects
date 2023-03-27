import sqlalchemy
import databases
import json

DATABASE_URL = "postgresql://root:BBHzCFOv9TbK1T0z31987RRa@alfie.iran.liara.ir:31794/postgres"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

uploads_table = sqlalchemy.Table(
    "uploads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("inputs", sqlalchemy.String),
    sqlalchemy.Column("language", sqlalchemy.String),
    sqlalchemy.Column("enable", sqlalchemy.Integer)
)

results_table = sqlalchemy.Table(
    "results",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("upload", sqlalchemy.Integer, sqlalchemy.ForeignKey("uploads.id")),
    sqlalchemy.Column("output", sqlalchemy.String, default="none"),
    sqlalchemy.Column("execute_date", sqlalchemy.String,default="none"),
    sqlalchemy.Column("filelink", sqlalchemy.String,default="none")
)

metadata.create_all(engine)


async def get_requests_by_email(email):
    try:
        async with database:
            query = uploads_table.select().where(uploads_table.c.email == email)
            results = await database.fetch_all(query)
            return [json.dumps(dict(row)) for row in results]
    except Exception as e:
        print(f"ERROR: Failed to get data from DB")
        print(f"Error message: {e}")
