from fastapi import FastAPI

app = FastAPI()

print("🔥 APP INICIANDO")

@app.get("/")
def root():
    return {"status": "running"}