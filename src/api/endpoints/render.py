import json
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, File, UploadFile
from fastapi.responses import FileResponse
import csv, time
from pydantic import BaseModel, Field, conint, model_validator
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client
from ..models import render

router = APIRouter()

reports_folder_path = "/opt/report-engine/code/data/reports/"
folder_path = "/opt/report-engine/code/data/renders/"
odt_renderer = get_odt_renderer(media_path=folder_path)

# Create PDF Report
@router.post("/render",summary="Creates a pdf report.", tags=["Render"])
def CreatePDFReport(report: render.ReportCreateRequest):
    timestamp = time.time()
    # RenderClass.render(body, timestamp)
    report_file_path = reports_folder_path + report.TemplateID
    rendered_file_path = folder_path + "rendered_%s.odt" % timestamp
    with ODTTemplate(report_file_path) as template:
        odt_renderer.render(
            template,
            context=report.Context,
        )
        template.pack(rendered_file_path)
    if (report.ConvertTo is None):
        return FileResponse(
            rendered_file_path,
            media_type="application/octet-stream",
            filename='%d.odt' % timestamp
        )
    # convert to pdf
    converted_file_path = folder_path + "converted_%s.pdf" % timestamp
    filter_options = []
    if (not report.Filtername is None):
        for k, v in report.FilterOptions.items():
            filter_options.append('%s=%s' % (k, v))
    uno = client.UnoClient(server='unoserver')
    convert_command = {
        'inpath': rendered_file_path,
        'outpath': converted_file_path,
        'convert_to': report.ConvertTo,
        'filtername': report.Filtername,
        'filter_options': filter_options
    }
    uno.convert(**convert_command)   
    return FileResponse(
        converted_file_path,
        filename='%d.pdf' % timestamp
    )

# Create PDF Report
@router.post("/render2",summary="Creates a pdf report.", tags=["Render"])
def CreatePDFReport2(images: list[UploadFile], report: render.ReportCreateRequest):
    return {"filenames": [file.filename for file in images]}

# Create PDF Report
@router.post("/render3",summary="Creates a pdf report.", tags=["Render"])
def CreatePDFReport3(report: render.ReportCreateRequest, image: UploadFile = File(...)):
    return {"filenames": [{image.filename}]}


class Rate(BaseModel):
    id1: int
    id2: int
    message: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

@router.post("/rate")
def submit(user_review: Rate = Body(...), image: UploadFile = File(...)):
        return {"JSON Payload ": user_review, "Image": image.filename}


class ReportCreateRequest(BaseModel):
    '''
    fileのアップロードと併用する場合、受け取った値をJsonで変換しなけらばならない。
    変換時に、Fieldのaliasを考慮する必要がある。
    → とりあえず、Field指定をしていない。
    '''
    template_id: str
    context: dict
    convert_to: str
    filtername: str
    filter_options: dict
    
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

@router.post("/rate2")
def submit2(user_review: ReportCreateRequest = Body(...), images: list[UploadFile] = File(...)):
        return {"JSON Payload ": user_review, "Image": [file.filename for file in images]}
