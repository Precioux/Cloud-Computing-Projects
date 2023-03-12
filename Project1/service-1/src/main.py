from typing import Union
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
import uvicorn
from api.rabbitmq import send
from api.s3 import download_file, upload_file
from db.postgres import database, engine, metadata

from db.postgres import uploads_table

app = FastAPI(title="service 1")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/submit_email/")
async def submit_email(id: int, email: str, inputs: str, language: str, enable: int, file: UploadFile = File(...)):
    #insert to db
    query = uploads_table.insert().values(id=id,
                                           email=email,
                                           inputs=inputs,
                                           language=language,
                                           enable=enable)

    await database.execute(query=query)
    address = str(id) + "." + file.filename.split(".")[-1]
    # await update_email(id, address=address)

    # save file on s3
    upload_file(file, address)

    # # put message on rabbitmq
    send(address)
    return f"Your submission was registered with ID: {id}"

@app.get("/check_email/")
async def check_email(id: int):
    query = uploads_table.select().where(uploads_table.c.id == id)
    result = await database.fetch_one(query=query)

    if not result:
        raise HTTPException(status_code=404, detail="Email not found")
    elif result["enable"] == 0:
        return {"status": True}
    else:
        return {"status": False}

@app.put("/update_email/")
async def update_email(id: int, state: Union[str, None] = None, category: Union[str, None] = None,
                               address: Union[str, None] = None):
    if (address):
        query = (
            uploads_table
                .update()
                .where(id == uploads_table.c.id)
                .values(address=address)
        )

    else:
        query = (
            uploads_table
                .update()
                .where(id == uploads_table.c.id)
                .values(state=state,
                        category=category)
        )
    await database.execute(query=query)


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)