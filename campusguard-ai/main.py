from fastapi import FastAPI, UploadFile, File
from analyzer import analyze_image
import shutil

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(file_path)
    return result

