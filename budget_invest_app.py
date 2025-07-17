import streamlit as st
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from botpress_client import BotpressClient
import os

# Botpress credentials via Streamlit secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]

# Initialize Botpress
bot_client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)

# ✅ FastAPI setup
api = FastAPI()

@api.post("/api/ask")
async def ask_bot(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    try:
        conv = bot_client.create_conversation()
        conv_id = conv["id"]
        bot_client.send_message(conv_id, user_message)
        reply = bot_client.list_messages(conv_id)
        messages = reply.get("messages", [])
        if messages:
            bot_reply = messages[-1].get("payload", {}).get("text", "No reply")
        else:
            bot_reply = "No messages returned."
        return JSONResponse(content={"reply": bot_reply})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ Streamlit UI (optional frontend)
st.set_page_config(page_title="💬 Budget Bot Assistant", layout="centered")
st.title("💬 Ask Your Budget Assistant")

user_input = st.text_input("Type your question:")
if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        conv = bot_client.create_conversation()
        conv_id = conv["id"]
        bot_client.send_message(conv_id, user_input)
        response = bot_client.list_messages(conv_id)
        messages = response.get("messages", [])
        if messages:
            reply = messages[-1].get("payload", {}).get("text", "No reply")
            st.success(reply)
        else:
            st.warning("No messages received.")

# ✅ Required for Streamlit Cloud to recognize FastAPI
def run():
    uvicorn.run(api, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()
