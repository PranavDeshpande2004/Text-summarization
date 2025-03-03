from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load the summarization model
summarizer = pipeline("summarization")

# Define request body model
class SummarizationRequest(BaseModel):
    text: str

@app.post("/api/summarize")
async def summarize_text(request: SummarizationRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # Generate summary
    summary = summarizer(request.text, max_length=50, min_length=10, do_sample=False)

    return {"summary": summary[0]["summary_text"]}

