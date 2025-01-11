from pydantic import BaseModel, Field

class ReportCreateRequest(BaseModel):
    TemplateID: str = Field(..., alias="template_id")
    Context: dict = Field(..., alias="context")
    ConvertTo: str = Field(default=None, alias="convert_to")
    Filtername: str = Field(default=None, alias="filtername")
    FilterOptions: dict = Field(default={}, alias="filter_options")
