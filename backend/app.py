from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq LLaMA-3 model
llm = ChatGroq(
    api_key="your_Api_key",  # ✅ Replace with your actual API key
    model="llama3-8b-8192",       # ✅ Use LLaMA-3 model
    temperature=0,                # ✅ Low temperature for deterministic output
    max_tokens=500                # ✅ Limit the output length
)

class TextRequest(BaseModel):
    text: str

@app.post("/api/summarize")
def summarize_text(request: TextRequest):
    try:
        response = llm.invoke(f"Summarize the following text:\n\n{request.text}")
        return {"summary": response.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI server with:
# uvicorn app:app --reload
