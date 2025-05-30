# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

from app.ssocr import predict  # ฟังก์ชันใหม่ที่คุณจะเพิ่ม

app = FastAPI()

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    temp_filename = f"/tmp/{uuid.uuid4()}.png"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = predict(temp_filename)
        return JSONResponse(content={"digits": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        os.remove(temp_filename)
