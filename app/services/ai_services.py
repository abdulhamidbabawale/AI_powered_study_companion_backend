
from fastapi import HTTPException
from app.gemini import client, GEMINI_MODEL, LEARNING_SYSTEM_PROMPT
from app.db.queries.chat_queries import create_chat, get_chat_by_id, append_message,get_chats
from app.db.models import ChatModel, MessageModel


async def send_message(user_id: str, message: str, chat_id: str = None):
    # 1. load or create chat
    if chat_id:
        chat = await get_chat_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        history = chat["messages"]
    else:
        history = []

    # 2. build contents — gemini expects list of dicts with role + parts
    contents = [
        {"role": msg["role"], "parts": [{"text": msg["content"]}]}
        for msg in history
    ]
    contents.append({"role": "user", "parts": [{"text": message}]})

    # 3. call gemini
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents
    )
    reply = response.text

    # 4. save messages to mongo
    user_message = MessageModel(role="user", content=message)
    model_message = MessageModel(role="model", content=reply)

    if not chat_id:
        new_chat = ChatModel(user_id=user_id, messages=[user_message, model_message])
        chat_id = await create_chat(new_chat)
    else:
        await append_message(chat_id, user_message)
        await append_message(chat_id, model_message)

    return {"chat_id": chat_id, "reply": reply}


async def fetch_chat(chat_id: str):
    return await get_chat_by_id(chat_id)

async def fetch_user_chats(user_id: str, page: int, limit: int):
    return await get_chats(user_id, page, limit)

# generate flashcards from uploaded content
async def generate_flashcards(content: str):
    prompt = f"""
    Based on the following learning material, generate 10 flashcards.
    Return them as a JSON array in this exact format, nothing else:
    [
        {{"question": "...", "answer": "..."}},
        {{"question": "...", "answer": "..."}}
    ]

    Learning material:
    {content}
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"system_instruction": LEARNING_SYSTEM_PROMPT}
    )

    import json
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)

# generate a summary from uploaded content
async def generate_summary(content: str):
    prompt = f"""
    Summarize the following learning material.
    Structure your response with:
    - A brief overview (2-3 sentences)
    - Key concepts (bullet points)
    - Important takeaways

    Learning material:
    {content}
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"system_instruction": LEARNING_SYSTEM_PROMPT}
    )

    return response.text

# answer a question based on material
async def answer_question(question: str, content: str, chat_id: str = None):
    message = f"""
    Using only the learning material below, answer this question:
    {question}

    Learning material:
    {content}
    """
    return await send_message(
        user_id=None,
        message=message,
        chat_id=chat_id
    )
