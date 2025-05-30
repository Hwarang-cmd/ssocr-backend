from fastapi import FastAPI, File, UploadFile
import uvicorn
import cv2
import numpy as np
import tempfile
from ssocr import load_image, preprocess, find_digits_positions, recognize_digits_line_method, THRESHOLD

app = FastAPI()

@app.post("/ocr")
async def read_7segment(file: UploadFile = File(...)):
    # Save uploaded image to a temp file
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    # Load image & process
    blurred, gray_img = load_image(tmp_path, show=False)
    dst = preprocess(blurred, THRESHOLD, show=False)
    digits_positions = find_digits_positions(dst)
    digits = recognize_digits_line_method(digits_positions, blurred, dst)

    return {"digits": ''.join(str(d) for d in digits)}
