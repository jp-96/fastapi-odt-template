import os
import re
import shutil
import tempfile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from jinja2 import Template
from pydantic import BaseModel, Field, model_validator
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from starlette.background import BackgroundTask
from typing import List, Optional
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
    file_basename: str = Field(default="rendered", description='The basename of the file (excluding the extension) to be used for the generated document.')
    convert_to_pdf: bool = Field(default=False, description='Indicates if the document should be converted to a PDF file.')
    pdf_filter_options: dict = Field(default={}, description='Options for the PDF export filter to be applied during conversion. See this link: https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html')

def cleanup_work_dir(work_folder_path: str):
    shutil.rmtree(work_folder_path)

prohibited_chars_pattern = r'[<>:"/\\|?*]'

def sanitize_filename(filename: str) -> str:
    sanitized_filename = re.sub(prohibited_chars_pattern, '_', filename)
    return sanitized_filename

@router.post("/odt",summary="render the report.", tags=["Render"])
def render(report_request: ReportGenerationRequest, template: UploadFile, images: Optional[List[UploadFile]]=File(None)):
    response_file_basename = report_request.file_basename if report_request.file_basename else "rendered"
    images = images or []
    # return {
    #     "payload": {
    #         "document_content": report_request.document_content,
    #         "file_basename": response_file_basename,
    #         "convert_to_pdf": report_request.convert_to_pdf,
    #         "pdf_filter_options": report_request.pdf_filter_options,
    #         "template": template.filename,
    #         "images": [file.filename for file in images]
    #     }
    # }

    # render basename
    response_file_basename = sanitize_filename(Template(response_file_basename).render(report_request.document_content))

    # work dir
    work_folder_path = tempfile.mkdtemp()
    media_folder_path = os.path.join(work_folder_path, "media")
    os.mkdir(media_folder_path)
    result_folder_path = os.path.join(work_folder_path, "result")
    os.mkdir(result_folder_path)

    # cleanup
    background_task = BackgroundTask(cleanup_work_dir, work_folder_path)

    # template
    try:
        template_file_path = os.path.join(work_folder_path, template.filename)
        with open(template_file_path, 'wb') as f:
            contents = template.file.read()
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the template file"}
    finally:
        template.file.close()
    
    # images
    for image in images:
        try:
            media_file_path = os.path.join(media_folder_path, image.filename)
            with open(media_file_path, 'wb') as f:
                contents = image.file.read()
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the image file"}
        finally:
            image.file.close()

    # render
    odt_result_file_path = os.path.join(result_folder_path, "rendered.odt")
    with ODTTemplate(template_file_path) as template:
        get_odt_renderer(media_folder_path).render(
            template,
            context=report_request.document_content,
        )
        template.pack(odt_result_file_path)
    if (report_request.convert_to_pdf != True):
        # ODT file response
        return FileResponse(
            path=odt_result_file_path,
            media_type="application/octet-stream",
            filename=response_file_basename + ".odt",
            background=background_task
        )
    
    # convert to pdf
    pdf_result_file_path = os.path.join(result_folder_path, "rendered.pdf")
    filter_options = []
    if (not report_request.pdf_filter_options is None):
        for k, v in report_request.pdf_filter_options.items():
            filter_options.append('%s=%s' % (k, v))
    filtername = None
    if (len(filter_options) > 0):
        filtername = "writer_pdf_Export"
    convert_command = {
        'inpath': odt_result_file_path,
        'outpath': pdf_result_file_path,
        'convert_to': "pdf",
        'filtername': filtername,
        'filter_options': filter_options
    }
    client.UnoClient(server='unoserver').convert(**convert_command)

    # PDF file response
    return FileResponse(
        path=pdf_result_file_path,
        filename=response_file_basename + ".pdf",
        background=background_task
    )
