from fastapi import FastAPI
from backend.api.routes import ticker
from backend.api.routes import industry
from backend.api.routes import time
from backend.api.routes import profitability
from backend.api.routes import risk
from backend.api.routes import analysis
from backend.api.routes import etl

app = FastAPI()

app.include_router(ticker.router)
app.include_router(industry.router)
app.include_router(time.router)
app.include_router(profitability.router)
app.include_router(risk.router)
app.include_router(analysis.router)
app.include_router(etl.router)