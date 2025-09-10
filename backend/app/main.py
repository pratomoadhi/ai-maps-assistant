from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Maps Assistant API")

# include routes from routes.py
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Maps Assistant API"}