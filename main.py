from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import subprocess

app = FastAPI()

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("input.pbm", thresh)

    result = subprocess.run(["./ssocr/ssocr", "input.pbm"], stdout=subprocess.PIPE)
    return {"result": result.stdout.decode().strip()}
