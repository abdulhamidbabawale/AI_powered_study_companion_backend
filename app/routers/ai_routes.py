from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_services import (
    send_message, fetch_chat, fetch_user_chats,
    generate_flashcards, generate_summary, answer_question,
    get_flashcards, get_summary,
)
from app.schemas.chat_schemas import (
    CreateChatSchema,AddMessageSchema,
    FlashcardRequest, SummaryRequest, QuestionRequest
)
from app.db.queries.material_queries import get_material_by_id,update_material
from app.jwt import get_current_user


router = APIRouter(prefix="/ai", tags=["ai"])


# # start a new chat
@router.post("/chat", status_code=201)
async def start_chat(body: CreateChatSchema,user_id: str = Depends(get_current_user)):
    result = await send_message(
        user_id=user_id,
        message=body.message
    )
    return {
        "message": "Chat started",
        "chat_id": result["chat_id"],
        "reply": result["reply"]
    }

# continue an existing chat
@router.post("/chat/{chat_id}")
async def continue_chat(chat_id: str, body: CreateChatSchema,user_id: str = Depends(get_current_user)):
    result = await send_message(
        user_id=user_id,
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
@router.get("/chats")
async def get_user_chats(user_id: str = Depends(get_current_user), page: int = 1, limit: int = 10):
    return await fetch_user_chats(user_id, page, limit)


# --- material-aware endpoints, all keyed by chat_id ---

@router.get("/flashcards/{chat_id}")
async def fetch_flashcards(chat_id: str, _: str = Depends(get_current_user)):
    flashcards = await get_flashcards(chat_id)
    return {"chat_id": chat_id, "flashcards": flashcards}

@router.get("/summary/{chat_id}")
async def fetch_summary(chat_id: str, _: str = Depends(get_current_user)):
    summary = await get_summary(chat_id)
    return {"chat_id": chat_id, "summary": summary}


@router.post("/ask/{chat_id}")
async def ask_question(chat_id: str, body: QuestionRequest, _: str = Depends(get_current_user)):
    try:
        result = await answer_question(body.question, chat_id)
        return {"chat_id": chat_id, "reply": result["reply"]}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
