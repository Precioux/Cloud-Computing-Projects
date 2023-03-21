import sqlalchemy
import databases

DATABASE_URL = "postgresql://root:BBHzCFOv9TbK1T0z31987RRa@alfie.iran.liara.ir:31794/postgres"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

jobs_table = sqlalchemy.Table(
    "jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("upload", sqlalchemy.Integer, sqlalchemy.ForeignKey("uploads.id")),
    sqlalchemy.Column("job", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String, default="none-executed")
)

metadata.create_all(engine)

uploads_table = sqlalchemy.Table(
    "uploads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("inputs", sqlalchemy.String),
    sqlalchemy.Column("language", sqlalchemy.String),
    sqlalchemy.Column("enable", sqlalchemy.Integer)
)

