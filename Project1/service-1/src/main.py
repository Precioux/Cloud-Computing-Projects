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


@app.get('/up')
async def up():
    return f"Hey!"


#curl -X POST -H "Content-Type: multipart/form-data" -F id=7 -F email="uni.mahdipour@gmail.com" -F inputs="" -F language="python" -F enable=0 -F file=@"C:\Users\Samin\Desktop\samin.py" http://localhost:8000/submit_email/
@app.post("/submit_email/")
async def submit_email(id: int, email: str, inputs: str, language: str, enable: int, file: UploadFile = File(...)):
    # insert to db
    query = uploads_table.insert().values(id=id,
                                          email=email,
                                          inputs=inputs,
                                          language=language,
                                          enable=enable)

    await database.execute(query=query)
    address = str(id) + "." + file.filename.split(".")[-1]
    # save file on s3
    upload_file(file, address)

    return f"Your submission was registered with ID: {id}"

#curl -X GET "http://localhost:8000/check_email/?id=5"
@app.get("/check_email/")
async def check_email(id: int):
    query = uploads_table.select().where(uploads_table.c.id == id)
    result = await database.fetch_one(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="Email not found")
    elif result["enable"] == 0:
        send(id)
    else:
        raise HTTPException(status_code=400, detail="You cannot request this code")


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
