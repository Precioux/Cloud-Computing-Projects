import sqlalchemy
import databases

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


metadata.create_all(engine)