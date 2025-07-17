# 📁 voice_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class VoiceInput(BaseModel):
    message: str

@app.post("/api/voice")
def voice_to_agent(input: VoiceInput):
    user_message = input.message

    # Example: Forward to your Streamlit agent or Botpress
    # This is a placeholder — replace with actual logic/API call
    streamlit_agent_url = os.getenv("STREAMLIT_AGENT_URL", "https://pafadvisor.streamlit.app")

    # In a real case, you could store, forward, or process this message
    print(f"🔁 Forwarding message to Streamlit agent: {user_message}")

    return {
        "reply": f"🧠 Received: '{user_message}'. This will be sent to your agent at {streamlit_agent_url}."
    }
