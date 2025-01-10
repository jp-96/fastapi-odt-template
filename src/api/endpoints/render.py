from fastapi import APIRouter
from fastapi.responses import FileResponse
import csv, time
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from ..models import render

router = APIRouter()

reports_folder_path = "/opt/report-engine/code/data/reports/"
folder_path = "/opt/report-engine/code/data/renders/"
odt_renderer = get_odt_renderer(media_path=folder_path)

# Lists all templates
# Create PDF Report
@router.post("/render",summary="Creates a pdf report.", tags=["Render"])
def CreatePDFReport(body: render.ReportCreateRequest):
    timestamp = time.time()
    # RenderClass.render(body, timestamp)
    report_file_path = reports_folder_path + body.TemplateID
    rendered_file_path = folder_path + "rendered_%s.odt" % timestamp
    with ODTTemplate(report_file_path) as template:
        odt_renderer.render(
            template,
            context={},
        )
        template.pack(rendered_file_path)
    return FileResponse(rendered_file_path, filename='%d.pdf' % timestamp)
