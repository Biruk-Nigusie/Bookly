from fastapi import FastAPI
from src.books.routes import router
version = "v1"
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server is starting...") # execute at start of server
    await init_db() # connect to db when app starts
    yield
    print("Server has been stopped") # This execute when server stops

app = FastAPI(
title="Bookly",
description="A REST API for a book review web service",
version=version,
lifespan=life_span # register life_span
)

app.include_router(router, prefix="/api/{version}/books", tags=["books"])