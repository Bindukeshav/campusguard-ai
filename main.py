from fastapi import FastAPI, UploadFile, File
from analyzer import analyze_image
from agent import investigate 
import shutil

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(file_path)

    investigated_findings =[]
    for finding in result["findings"]:
        if finding["status"] in ["suspicious","possible_fall"]:
            investigation = investigate(finding)
            investigated_findings.append(investigation)

        else:
            investigated_findings.append({
                "finding":finding,
                "serverity":"low",
                "report":"No action needed."

            })
    return {
        "people_count" : result["people_count"],
        "bags_count":result["bags_count"],
        "findidngs":investigated_findings
    } 


    return result

