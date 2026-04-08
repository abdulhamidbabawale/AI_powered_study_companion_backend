from app.db.queries.user_queries import create_user, get_user_by_email
import bcrypt
from app.schemas.user_schemas import CreateUserSchema, LoginSchema
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from app.db.models import UserModel
from app.jwt import create_access_token


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

async def register_user(user:CreateUserSchema):

    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed = hash_password(user.password)

    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_no=user.phone_no,
        hashed_password=hashed,  
        role=user.role
    )

    save_new_user= await create_user(new_user)
    return save_new_user


async def login_user(credentials: LoginSchema):
    # 1. find user
    user = await get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 2. verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. check account is active
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account is disabled")

    # 4. generate token
    token = create_access_token(data={
        "sub": user["_id"],
        "email": user["email"],
        "role": user["role"]
    })

    return token