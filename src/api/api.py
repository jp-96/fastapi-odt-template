from fastapi import APIRouter
from .endpoints import report, render, renderimg

api_router = APIRouter()
api_router.include_router(render.router, tags=["Render"])
api_router.include_router(renderimg.router, tags=["Render"])
api_router.include_router(report.router, tags=["Report"])
