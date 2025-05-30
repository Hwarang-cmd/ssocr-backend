from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from ssocr import recognize_digit

app = FastAPI()

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

    digit = recognize_digit(img)
    return {"digit": digit}
