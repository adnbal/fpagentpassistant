# 👇 Add this at the top
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import streamlit as st
from botpress_client import BotpressClient
import os

# ✅ Botpress credentials from environment or hardcode (for now)
BOTPRESS_API_ID = os.getenv("BOTPRESS_API_ID", "your_botpress_api_id")
BOTPRESS_TOKEN = os.getenv("BOTPRESS_TOKEN", "your_botpress_token")
bp_client = BotpressClient(api_id=BOTPRESS_API_ID, user_key=BOTPRESS_TOKEN)

# 👇 FastAPI setup
api = FastAPI()

class Query(BaseModel):
    message: str

@api.post("/api/ask")
def ask(query: Query):
    convo = bp_client.create_conversation()
    conv_id = convo['id']
    bp_client.send_message(conv_id, query.message)
    messages = bp_client.list_messages(conv_id)
    last_reply = messages[-1]["payload"]["text"]
    return {"response": last_reply}

# 👇 Streamlit app
st.set_page_config(page_title="💸 Budgeting + Investment Planner")
st.title("💸 Budgeting & Investment Assistant")

user_query = st.text_input("Ask a question")
if user_query:
    convo = bp_client.create_conversation()
    conv_id = convo['id']
    bp_client.send_message(conv_id, user_query)
    messages = bp_client.list_messages(conv_id)
    last_reply = messages[-1]["payload"]["text"]
    st.write(last_reply)

# 👇 For standalone API dev
if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
