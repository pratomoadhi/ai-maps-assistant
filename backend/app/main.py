from fastapi import FastAPI, Request
from app.routes import router
from app.core import limiter, logger
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(title="Maps Assistant API")

# Add limiter state + error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routes
app.include_router(router)

@app.get("/")
@limiter.limit("10/minute")  # example: max 10 requests per minute per IP
async def root(request: Request):
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Maps Assistant API"}
