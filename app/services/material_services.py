from fastapi import UploadFile, HTTPException, BackgroundTasks
from app.db.queries.material_queries import save_material, update_material
from app.db.queries.chat_queries import create_chat
from app.db.models import MaterialModel, ChatModel
from app.services.ai_services import generate_flashcards, generate_summary
from app.services.file_services import extract_text_from_pdf, extract_text_from_pptx


async def process_upload(file: UploadFile, user_id: str, background_tasks: BackgroundTasks):
    # 1. check file type
    if file.filename.endswith(".pdf"):
        file_type = "pdf"
    elif file.filename.endswith(".pptx"):
        file_type = "pptx"
    else:
        raise HTTPException(status_code=400, detail="Only PDF and PPTX files are supported")

    # 2. extract text
    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes) if file_type == "pdf" else extract_text_from_pptx(file_bytes)

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    # 3. create a chat tied to this material
    chat = ChatModel(
        user_id=user_id,
        title=file.filename,       # chat title = filename
    )
    chat_id = await create_chat(chat)

    # 4. save material with chat_id
    material = MaterialModel(
        user_id=user_id,
        chat_id=chat_id,
        title=file.filename,
        file_type=file_type,
        raw_text=raw_text,
    )
    material_id = await save_material(material)

    # 5. generate summary + flashcards in background
    background_tasks.add_task(generate_ai_content, material_id, raw_text)

    return {
        "material_id": material_id,
        "chat_id": chat_id,
        "title": file.filename,
        "processing_status": "processing",
        "message": "File uploaded. Summary and flashcards are being generated."
    }


async def generate_ai_content(material_id: str, raw_text: str):
    try:
        summary = await generate_summary(raw_text)
        flashcards = await generate_flashcards(raw_text)
        await update_material(material_id, {
            "summary": summary,
            "flashcards": flashcards,
            "processing_status": "done"
        })
    except Exception as e:
        await update_material(material_id, {
            "processing_status": "failed",
            "processing_error": str(e)
        })