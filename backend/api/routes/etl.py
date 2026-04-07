from fastapi import APIRouter
from etl.load.load import run_etl

router = APIRouter()

@router.post("/etl/run")
def trigger_etl():
    run_etl()
    return {"status": "ETL completed"}