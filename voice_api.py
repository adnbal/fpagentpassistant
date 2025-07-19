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
