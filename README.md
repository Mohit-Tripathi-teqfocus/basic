# Crypto Market API

A simple FastAPI project that fetches cryptocurrency data using the CoinGecko API.

## Features
- List coins with pagination
- List categories
- Filter coins by ID or category
- CAD currency display
- Health check and version info endpoints
- Dockerized


## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file:

```env
COINGECKO_API_BASE=https://api.coingecko.com/api/v3
DEFAULT_CURRENCY=cad
```

API available at: `http://127.0.0.1:8000/docs`

## Health & Metadata
- `GET /health` → basic server check
- `GET /version` → app + 3rd-party API info

## Docker Usage

### Build and Run
```bash
docker build -t crypto-api .
docker run -d -p 8000:8000 crypto-api
```

### Or with Docker Compose
```bash
docker-compose up --build
```

## Linting & Formatting

```bash
black .
isort .
```

## Testing

```bash
pytest --cov=app
```

To generate a coverage report, install `pytest-cov`:

```bash
pip install pytest-cov
```

Then run:

```bash
pytest --cov=app --cov-report=term-missing
```