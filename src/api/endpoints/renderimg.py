import os
import time
from typing import List, Optional
from fastapi import APIRouter, File, Path, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client

router = APIRouter()

temp_folder_path = "/opt/report-engine/code/data/renders/"
media_path = temp_folder_path + "media/"
odt_renderer = get_odt_renderer(media_path)

class ReportCreateRequest(BaseModel):
    context: dict = Field(default={})
    convert_to: str = Field(default=None)
    filtername: str = Field(default=None)
    filter_options: dict = Field(default={})

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value

# Create PDF Report
@router.post("/renderimg",summary="Creates a pdf report.", tags=["RenderImg"])
def CreatePDFReport(report: ReportCreateRequest, template: UploadFile, images: Optional[List[UploadFile]]=File(None)):
    timestamp = time.time()
    try:
        contents = template.file.read()
        name = template.filename.replace(" ", "_")
        name = template.filename.replace("-", "_")
        report_file_path = temp_folder_path + name
        with open(report_file_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the template file"}
    finally:
        template.file.close()
    
    if images is None:
        images = []
    for image in images:
        try:
            contents = image.file.read()
            name = image.filename.replace(" ", "_")
            name = image.filename.replace("-", "_")
            media_file_path = media_path + name
            with open(media_file_path, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the image file"}
        finally:
            image.file.close()

    rendered_file_path = temp_folder_path + "rendered_%s.odt" % timestamp
    with ODTTemplate(report_file_path) as template:
        odt_renderer.render(
            template,
            context=report.context,
        )
        template.pack(rendered_file_path)
    if (report.convert_to is None):
        return FileResponse(
            rendered_file_path,
            media_type="application/octet-stream",
            filename='%d.odt' % timestamp
        )
    # convert to pdf
    converted_file_path = temp_folder_path + "converted_%s.pdf" % timestamp
    filter_options = []
    if (not report.filtername is None):
        for k, v in report.filter_options.items():
            filter_options.append('%s=%s' % (k, v))
    uno = client.UnoClient(server='unoserver')
    convert_command = {
        'inpath': rendered_file_path,
        'outpath': converted_file_path,
        'convert_to': report.convert_to,
        'filtername': report.filtername,
        'filter_options': filter_options
    }
    uno.convert(**convert_command)   
    return FileResponse(
        converted_file_path,
        filename='%d.pdf' % timestamp
    )
