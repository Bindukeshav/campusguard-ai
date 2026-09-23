import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from analyzer import analyze_and_draw  # rename analyze_image.py -> analyzer.py, or adjust this import

app = FastAPI()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.post("/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    # Unique filenames per request so concurrent uploads don't overwrite each other
    request_id = uuid.uuid4().hex
    file_path = UPLOAD_DIR / f"{request_id}_{file.filename}"
    output_path = OUTPUT_DIR / f"{request_id}_output.jpg"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_and_draw(str(file_path), str(output_path))

    return FileResponse(result["output_path"], media_type="image/jpeg")