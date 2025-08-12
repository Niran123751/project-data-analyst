from fastapi import FastAPI, File, UploadFile, Form
from utils import handle_question
import uvicorn
import json

app = FastAPI()

@app.post("/api/")
async def analyze(
    questions: UploadFile = File(...),
    files: list[UploadFile] = []
):
    # Read question text
    question_text = (await questions.read()).decode("utf-8")

    # Read optional attachments
    attachments = {}
    for f in files:
        attachments[f.filename] = await f.read()

    # Process with our data analyst logic
    answer = handle_question(question_text, attachments)

    return answer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
