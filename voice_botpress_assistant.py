from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Dummy agent logic to simulate a reply
def run_budget_agent(user_input: str) -> str:
    if "invest" in user_input.lower():
        return "Based on your savings, I recommend looking into low-risk ETFs this month."
    elif "budget" in user_input.lower():
        return "You're spending 70% of your income. Try to reduce dining out expenses."
    else:
        return "I'm here to help with your budget or investment questions!"

# FastAPI setup
app = FastAPI()

# Allow requests from anywhere (CORS policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for the incoming POST request
class VoiceInput(BaseModel):
    text: str

# API endpoint for receiving voice input from Android app
@app.post("/api/voice")
async def handle_voice_input(data: VoiceInput):
    user_text = data.text
    reply = run_budget_agent(user_text)
    return {"reply": reply}
