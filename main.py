from fastapi import FastAPI
from api.v1.router import v1_router
from contextlib import asynccontextmanager
from database.session import create_tables


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
    return {"message": "OK"}
