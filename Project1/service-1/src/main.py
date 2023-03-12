from typing import Union
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
import uvicorn
# from api.rabbitmq import send
# from api.s3 import download_file, upload_file
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
    # insert to db
    query = uploads_table.insert().values(id=id,
                                           email=email,
                                           inputs=inputs,
                                           language=language,
                                           enable=enable)

    await database.execute(query=query)
    # address = str(id) + "." + file.filename.split(".")[-1]
    # await update_email(id, address=address)
    #
    # # save file on s3
    # upload_file(file, address)
    #
    # # put message on rabbitmq
    # send(address)

    # # save program inputs to a file
    # inputs_address = str(id) + ".txt"
    # with open(inputs_address, "w") as f:
    #     f.write(inputs)
    # upload_file(inputs_address, inputs_address)

    return f"Your submission was registered with ID: {id}"




# @app.get("/get_advertisement_output/{id}")
# async def get_advertisement(id: int):
#     query = uploads_table.select().where(uploads_table.c.id == id)
#     advertisement = await database.fetch_one(query)
#     if (advertisement == None):
#         return None
#
#     if (advertisement.state == "confirmed"):
#         result = {"category": advertisement.category,
#                   "description": advertisement.description}
#         suffix = advertisement.address.split('.')[-1]
#         add = f"./img/output.{suffix}"
#         download_file(advertisement.address, add)
#         cv2img = cv2.imread(add)
#         res, im_png = cv2.imencode(f"output.{suffix}", cv2img)
#         response = Response(content=im_png.tobytes(), headers=result, media_type="image/jpg")
#
#         return response
#
#     if (advertisement.state == "denied"):
#         return {"result": "Your ad was not approved"}
#
#     if (advertisement.state == "pending"):
#         return {"result": "Your ad is processing"}


# @app.get("/get_email/{id}")
# async def get_email(id: int):
#     query = uploads_table.select().where(uploads_table.c.id == id)
#     advertisement = await database.fetch_one(query)
#     return advertisement


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