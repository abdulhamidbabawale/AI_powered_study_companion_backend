from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from app.services.material_services import process_upload
from app.db.queries.material_queries import get_material_by_id, get_user_materials
from app.jwt import get_current_user

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("/upload", status_code=201)
async def upload_material(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user_id: str = Depends(get_current_user)
):
    return await process_upload(file, user_id, background_tasks)

@router.get("/{material_id}")
async def get_material(material_id: str, _: str = Depends(get_current_user)):
    return await get_material_by_id(material_id)

@router.get("/user/all")
async def get_materials(user_id: str = Depends(get_current_user), page: int = 1, limit: int = 10):
    return await get_user_materials(user_id, page, limit)