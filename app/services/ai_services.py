
from fastapi import HTTPException
from app.gemini import client, GEMINI_MODEL, LEARNING_SYSTEM_PROMPT, generate_with_retry
from app.db.queries.chat_queries import create_chat, get_chat_by_id, append_message,get_chats
from app.db.queries.material_queries import get_material_by_chat_id, update_material
from app.db.models import ChatModel, MessageModel
import json


async def send_message(user_id: str, message: str,user_question:str=None, chat_id: str = None):
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
    # reply = await generate_with_retry(contents) 
    reply = response.text

    # 4. save messages to mongo
    if user_question:
       user_message = MessageModel(role="user", content=user_question)
    else:
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
async def get_flashcards(chat_id: str):
    material = await get_material_by_chat_id(chat_id)

    # return stored if already generated
    if material.get("flashcards") and material.get("processing_status") == "done":
        return material["flashcards"]

    if material.get("processing_status") == "processing":
        raise HTTPException(status_code=202, detail="Flashcards are still being generated, try again shortly")

    # fallback: regenerate if failed
    flashcards = await generate_flashcards(material["raw_text"])
    await update_material(material["_id"], {"flashcards": flashcards, "processing_status": "done"})
    return flashcards


async def get_summary(chat_id: str):
    material = await get_material_by_chat_id(chat_id)

    if material.get("summary") and material.get("processing_status") == "done":
        return material["summary"]

    if material.get("processing_status") == "processing":
        raise HTTPException(status_code=202, detail="Summary is still being generated, try again shortly")

    summary = await generate_summary(material["raw_text"])
    await update_material(material["_id"], {"summary": summary, "processing_status": "done"})
    return summary


async def answer_question(question: str, chat_id: str):
    material = await get_material_by_chat_id(chat_id)
    raw_text = material["raw_text"]
    user_id = material["user_id"]

    message = f"""
    Using only the learning material below, answer this question:
    {question}

    Learning material:
    {raw_text}
    """
    return await send_message(user_id=user_id, message=message,user_question=question, chat_id=chat_id)


# --- internal helpers ---

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
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)


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