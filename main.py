# app/main.py
from fastapi import FastAPI
from core.routes import upload, query

app = FastAPI()

app.include_router(upload.router)
app.include_router(query.router)