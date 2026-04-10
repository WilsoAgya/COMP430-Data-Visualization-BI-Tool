# COMP430 Data Visualization BI Tool

Deployed URL: https://comp430.jakobupton.dev/

A full-stack business intelligence dashboard for exploring stock market data.

The project currently includes:
- A React + TypeScript frontend built with Vite, Tailwind CSS, and shadcn/ui
- A FastAPI backend that serves stock, ticker, and dimensional data from PostgreSQL
- ETL scripts for extracting and transforming source market data

## Repository Layout

```text
frontend/   React dashboard UI
backend/    FastAPI application
etl/        Extract / transform / load scripts
```

## Current Features

- Ticker-based routes such as `/ticker/AAPL`
- Backend-powered ticker search by symbol or company name
- Area chart with backend range queries for `1M`, `3M`, `6M`, and `1Y`
- Chart tooltip to view high/low prices on any day within the range
- News panel powered by NewsAPI

## Tech Stack

Frontend:
- React 19
- TypeScript
- Vite
- Tailwind CSS v4
- shadcn/ui
- Recharts
- React Router

Backend:
- FastAPI
- Uvicorn
- psycopg2
- python-dotenv

Data:
- PostgreSQL
- pandas
- requests
- yfinance

## Prerequisites

Frontend:
- Node.js 20+
- npm

Backend:
- Python 3.11+
- PostgreSQL database with the expected BI tables

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Useful frontend scripts:

```bash
npm run build
npm run lint
npm run format
npm run format:check
```

### Frontend Environment

For the news tab, create `frontend/.env.local` with:

```env
news_api_key=your_newsapi_key_here
```

## Backend Setup

Create a virtual environment and install dependencies:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn psycopg2-binary python-dotenv pandas requests yfinance
```

Run the API from the repository root so Python can resolve the `backend.*` imports:

```bash
cd ..
backend/.venv/bin/python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000
```

### Backend Environment

The backend expects database settings from a `.env` file. Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=comp430
DB_USER=postgres
DB_PASSWORD=postgres
DB_SSLMODE=disable
```

## API Routes

Implemented routes include:

- `GET /tickers?q=AAPL&limit=8`
- `GET /stocks/{symbol}?range=1M|3M|6M|1Y`
- `GET /industries`
- `GET /analysis`
- `GET /risk`
- `GET /time`
- `GET /profitability`
- `POST /etl/run`

The frontend expects the backend to be exposed behind `/api`, for example:
- frontend request: `/api/stocks/AAPL?range=6M`
- proxied backend request: `http://127.0.0.1:8000/stocks/AAPL?range=6M`

## Our Deployment Notes

Somethings we relied on for our deployment was:
- `systemd` to keep the FastAPI backend and node frontend alive
- `nginx` to serve the frontend build and reverse-proxy `/api` to FastAPI
- `cloudflare` to route our DNS
- `traefik` for routing our local IP address through to cloudflare
- `proxmox` for containerization of our postgres & backend/frontend combo
