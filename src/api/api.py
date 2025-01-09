from fastapi import APIRouter
from .report import report

api_router = APIRouter()
api_router.include_router(report.router, tags=["Report"])
