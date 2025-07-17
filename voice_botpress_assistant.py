from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from botpress_client import run_botpress_agent  # your logic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceQuery(BaseModel):
    text: str

@app.post("/api/voice")
def handle_voice(query: VoiceQuery):
    reply = run_botpress_agent(query.text)
    return {"reply": reply}
