from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_services import (
    send_message, fetch_chat, fetch_user_chats,
    generate_flashcards, generate_summary, answer_question
)
from app.schemas.chat_schemas import (
    CreateChatSchema,AddMessageSchema,
    FlashcardRequest, SummaryRequest, QuestionRequest
)


router = APIRouter(prefix="/ai", tags=["ai"])


# start a new chat
@router.post("/chat", status_code=201)
async def start_chat(body: CreateChatSchema):
    result = await send_message(
        user_id=body.user_id,
        message=body.message
    )
    return {
        "message": "Chat started",
        "chat_id": result["chat_id"],
        "reply": result["reply"]
    }

# continue an existing chat
@router.post("/chat/{chat_id}")
async def continue_chat(chat_id: str, body: AddMessageSchema):
    result = await send_message(
        user_id=body.user_id,
        message=body.message,
        chat_id=chat_id
    )
    return {
        "chat_id": result["chat_id"],
        "reply": result["reply"]
    }

# get a single chat with all messages
@router.get("/chat/{chat_id}")
async def get_chat(chat_id: str):
    chat = await fetch_chat(chat_id)
    return chat

# get all chats for a user (paginated)
@router.get("/chats/{user_id}")
async def get_user_chats(user_id: str, page: int = 1, limit: int = 10):
    return await fetch_user_chats(user_id, page, limit)


@router.post("/flashcards")
async def create_flashcards(body: FlashcardRequest):
    flashcards = await generate_flashcards(body.content)
    return {
        "user_id": body.user_id,
        "flashcards": flashcards
    }

@router.post("/summary")
async def create_summary(body: SummaryRequest):
    summary = await generate_summary(body.content)
    return {
        "user_id": body.user_id,
        "summary": summary
    }

@router.post("/ask")
async def ask_question(body: QuestionRequest):
    result = await answer_question(body.question, body.content, body.chat_id)
    return {
        "reply": result["reply"],
        "chat_id": result["chat_id"]
    }