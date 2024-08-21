from faker import Faker
from urllib.parse import unquote
from api.v1.router import v1_router
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from database.session import create_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from utils.hashing import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Media fayllarni saqlash uchun papka
MEDIA_DIR = "media"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="FastAPI",
    description="FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(v1_router)


@app.get("/")
async def root():
    return {"message": "Success"}


@app.get("/media/{path:path}")
async def read_media(path: str):
    file_path = unquote(f"{MEDIA_DIR}/{path}")
    return FileResponse(file_path)

fake = Faker()


@app.post("/users_post")
async def post_multiple_users(count: int, session: AsyncSession = Depends(get_async_session)):
    users = []
    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = fake.random_number(digits=13, fix_len=True)
        username = fake.user_name()
        password = fake.password()

        hashed_password = hash_password(password)  # password should be hashed

        user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=username,
            hashed_password=hashed_password
        )

        users.append(user)

    session.add_all(users)
    await session.commit()

    return {"message": f"{count} users created successfully"}
