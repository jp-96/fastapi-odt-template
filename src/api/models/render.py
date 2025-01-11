from pydantic import BaseModel, Field
import typing

class ReportCreateRequest(BaseModel):
    Context: dict = Field(alias="context")
    TemplateID: str = Field(alias="template_id")
