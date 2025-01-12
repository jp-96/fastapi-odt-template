from pydantic import BaseModel, Field, field_validator, model_validator

class JsonBaseModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value

class ReportCreateRequest(BaseModel):
    TemplateID: str = Field(..., alias="template_id")
    Context: dict = Field(..., alias="context")
    ConvertTo: str = Field(default=None, alias="convert_to")
    Filtername: str = Field(default=None, alias="filtername")
    FilterOptions: dict = Field(default={}, alias="filter_options")

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value
    
    @field_validator("Context", mode='before')
    @classmethod
    def validate_to_json_context(cls, value):
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value
