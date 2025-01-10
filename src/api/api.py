from fastapi import APIRouter
from .endpoints import report, render

api_router = APIRouter()
api_router.include_router(report.router, tags=["Report"])
api_router.include_router(render.router, tags=["Render"])
