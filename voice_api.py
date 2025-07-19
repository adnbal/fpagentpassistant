from fastapi import FastAPI
from pydantic import BaseModel
import os
from botpress_client import BotpressClient

app = FastAPI()

API_ID = os.getenv("BOTPRESS_CHAT_API_ID") or "bot_16e43556-ccfc-4fea-b39b-a9eefac04ef3"
USER_KEY = os.getenv("BOTPRESS_TOKEN") or "bp_pat_hkH6xKDFL4ddPurtB4qgVYumQKmFv8MHeEFB"

class VoiceInput(BaseModel):
    text: str

@app.post("/api/voice")
async def handle_voice_input(data: VoiceInput):
    user_text = data.text
    bot_client = BotpressClient(api_id=API_ID, user_key=USER_KEY)
    conv = bot_client.create_conversation()
    conv_id = conv["id"]
    bot_client.send_message(conv_id, user_text)
    response = bot_client.list_messages(conv_id)
    
    # Extract last reply
    messages = response.get("messages", [])
    if messages:
        for m in reversed(messages):
            if m["type"] == "text" and m["role"] == "assistant":
                return {"reply": m["text"]}
    return {"reply": "No reply from Botpress."}
