import os
import time
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client

router = APIRouter()
class JsonBaseModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def validate_json(cls, value):
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value

class ReportGenerationRequest(JsonBaseModel):
    document_content: dict = Field(default={}, description='The content of the document to be rendered.')
    convert_to_pdf: bool = Field(default=False, description='Indicates if the document should be converted to a PDF file.')
    pdf_filter_options: dict = Field(default={}, description='Options for the PDF export filter to be applied during conversion. See this link: https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html')

@router.post("/odt",summary="render the report.", tags=["Render"])
def render(report_request: ReportGenerationRequest, template: UploadFile, images: Optional[List[UploadFile]]=File(None)):
    if images is None:
        images = []
    # return {"JSON Payload": report_request, "template": template.filename, "images": [file.filename for file in images]}

    timestamp = time.time()
    temp_folder_path = "/opt/report-engine/code/data/renders/%s/" % timestamp
    os.mkdir(temp_folder_path)
    media_folder_path = temp_folder_path + "media/"
    os.mkdir(media_folder_path)

    try:
        contents = template.file.read()
        name = template.filename.replace(" ", "_")
        name = template.filename.replace("-", "_")
        template_file_path = temp_folder_path + name
        with open(template_file_path, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the template file"}
    finally:
        template.file.close()
    
    for image in images:
        try:
            contents = image.file.read()
            name = image.filename.replace(" ", "_")
            name = image.filename.replace("-", "_")
            media_file_path = media_folder_path + name
            with open(media_file_path, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the image file"}
        finally:
            image.file.close()

    rendered_file_path = temp_folder_path + "rendered_%s.odt" % timestamp
    with ODTTemplate(template_file_path) as template:
        get_odt_renderer(media_folder_path).render(
            template,
            context=report_request.document_content,
        )
        template.pack(rendered_file_path)
    if (report_request.convert_to_pdf != True):
        return FileResponse(
            rendered_file_path,
            media_type="application/octet-stream",
            filename='%d.odt' % timestamp
        )
    
    # convert to pdf
    filter_options = []
    if (not report_request.pdf_filter_options is None):
        for k, v in report_request.pdf_filter_options.items():
            filter_options.append('%s=%s' % (k, v))
    filtername = None
    if (len(filter_options) > 0):
        filtername = "writer_pdf_Export"
    
    converted_file_path = temp_folder_path + "converted_%s.pdf" % timestamp
    convert_command = {
        'inpath': rendered_file_path,
        'outpath': converted_file_path,
        'convert_to': "pdf",
        'filtername': filtername,
        'filter_options': filter_options
    }
    client.UnoClient(server='unoserver').convert(**convert_command)

    return FileResponse(
        converted_file_path,
        filename='%d.pdf' % timestamp
    )
