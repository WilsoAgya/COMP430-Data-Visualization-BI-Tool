from fastapi import FastAPI
from api.routes import ticker, industry, time, profitability, risk, analysis, etl

app = FastAPI()

app.include_router(ticker.router)
app.include_router(industry.router)
app.include_router(time.router)
app.include_router(profitability.router)
app.include_router(risk.router)
app.include_router(analysis.router)
app.include_router(etl.router)