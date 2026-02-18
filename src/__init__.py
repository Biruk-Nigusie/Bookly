from fastapi import FastAPI
from src.books.routes import router
version = "v1"
app = FastAPI(
title="Bookly",
description="A REST API for a book review web service",
version=version,
)

app.include_router(router, prefix="/api/{version}/books", tags=["books"])