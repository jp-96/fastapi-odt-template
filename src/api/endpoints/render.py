from fastapi import APIRouter
from fastapi.responses import FileResponse
import csv, time
from ..models import render

router = APIRouter()

# Crete PDF Report
@router.post("/render",summary="Creates a pdf report.", tags=["Render"])
def CreatePDFReport(body: render.ReportCreateRequest):
    timestamp = time.time()
    # RenderClass.render(body, timestamp)
    # return FileResponse(Converter.docx2pdf(timestamp), filename='%d.pdf' % timestamp)
