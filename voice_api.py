from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceInput(BaseModel):
    text: str

@app.post("/api/voice")
async def handle_voice(data: VoiceInput):
    return {"reply": f"You said: {data.text}"}
