from fastapi import FastAPI
from app.routes import upload, query

app = FastAPI()

print("🔥 APP INICIANDO")

# 🔥 registra os routers
app.include_router(upload.router)
app.include_router(query.router)


@app.get("/")
def root():
    return {"status": "running"}