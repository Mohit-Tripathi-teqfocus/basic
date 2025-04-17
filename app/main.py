from fastapi import FastAPI
from app.routes import coins
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Crypto Market API")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/version")
def version_info():
    """Version and service metadata endpoint."""
    return {
        "app_version": "1.0.0",
        "coingecko_api": os.getenv("COINGECKO_API_BASE", "not set"),
    }


app.include_router(coins.router, prefix="/api")
