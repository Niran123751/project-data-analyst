from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Data Analyst Agent API is running"}

@app.post("/api/")
async def analyze(
    questions: UploadFile = File(...),
    file1: UploadFile = File(None),
    file2: UploadFile = File(None)
):
    # Read questions.txt
    q_text = (await questions.read()).decode("utf-8")

    # Example: process CSV if provided
    csv_data = None
    if file1 and file1.filename.endswith(".csv"):
        csv_data = pd.read_csv(io.BytesIO(await file1.read())).to_dict()

    return {
        "questions": q_text,
        "csv_preview": csv_data
    }
