from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
from ssocr import load_image, preprocess, find_digits_positions, recognize_digits_line_method, THRESHOLD

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}.png"
    filepath = f"./{filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        blurred, gray_img = load_image(filepath)
        processed_img = preprocess(blurred, THRESHOLD)
        digits_positions = find_digits_positions(processed_img)
        digits = recognize_digits_line_method(digits_positions, blurred, processed_img)
        return {"digits": digits}
    finally:
        os.remove(filepath)
