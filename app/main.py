from fastapi import FastAPI
from app.routes import coins
from dotenv import load_dotenv
import os
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

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


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


app.include_router(coins.router, prefix="/api")
