from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
from app.ssocr import load_image, preprocess, find_digits_positions, recognize_digits_line_method
import cv2

app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Save file temporarily
    tmp_filename = f"temp_{uuid.uuid4()}.png"
    with open(tmp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process image
    blurred, _ = load_image(tmp_filename)
    preprocessed = preprocess(blurred, 35)
    positions = find_digits_positions(preprocessed)
    digits = recognize_digits_line_method(positions, blurred, preprocessed)

    # Cleanup
    os.remove(tmp_filename)

    return {"digits": digits}
