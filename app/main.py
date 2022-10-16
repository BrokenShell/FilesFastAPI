import os

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.aws_s3 import S3


API = FastAPI(
    title='FilesFastAPI',
    version="0.0.1",
    docs_url='/',
)

API.s3 = S3()

API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.put("/upload")
async def upload(file: UploadFile = File(...)):
    API.s3.upload(file)
    return True


@API.get("/download/{filename}")
async def download(filename: str):
    filepath = os.path.join(f"{API.s3.directory}", filename)
    if not os.path.exists(filepath):
        API.s3.download(filename)
    return FileResponse(filepath, filename=filename)


@API.delete("/delete/{filename}")
async def delete(filename: str):
    API.s3.delete(filename)
    filepath = os.path.join(f"{API.s3.directory}", filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return True
