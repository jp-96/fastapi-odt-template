from fastapi import APIRouter
from fastapi.responses import FileResponse
import csv, time
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client
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
            context=body.Context,
        )
        template.pack(rendered_file_path)
    if (body.ConvertTo is None):
        return FileResponse(
            rendered_file_path,
            media_type="application/octet-stream",
            filename='%d.odt' % timestamp
        )
    # convert to pdf
    converted_file_path = folder_path + "converted_%s.pdf" % timestamp
    filter_options = []
    if (not body.Filtername is None):
        for k, v in body.FilterOptions.items():
            filter_options.append('%s=%s' % (k, v))
    uno = client.UnoClient(server='unoserver')
    convert_command = {
        'inpath': rendered_file_path,
        'outpath': converted_file_path,
        'convert_to': body.ConvertTo,
        'filtername': body.Filtername,
        'filter_options': filter_options
    }
    uno.convert(**convert_command)   
    return FileResponse(
        converted_file_path,
        filename='%d.pdf' % timestamp
    )
