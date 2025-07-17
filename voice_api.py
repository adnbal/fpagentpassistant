
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS setup to allow Android apps to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceInput(BaseModel):
    message: str

@app.post("/api/voice")
async def process_voice(input: VoiceInput):
    user_message = input.message

    # Send to your Streamlit Agent or Gemini/DeepSeek endpoint
    # Replace below with your actual logic
    response = requests.post(
        "https://pafadvisor.streamlit.app/your-api-endpoint",  # ❗Replace with actual endpoint if exists
        json={"query": user_message}
    )

    if response.status_code == 200:
        return {"reply": response.json().get("response", "🧠 No detailed reply returned.")}
    else:
        return {"reply": "⚠️ Error contacting AI agent."}
