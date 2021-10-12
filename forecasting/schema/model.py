from pydantic import BaseModel, Field, EmailStr, ValidationError, validator, root_validator
import datetime


class Upload(BaseModel):
    project_name: str = Field(title="The project name")
    project_description: str = Field(
        title="The project description")
    creation_date: str = Field(default=datetime.datetime.now())

    def upload_output(self):
        return {
            "project_name": self.project_name,
            "project_description": self.project_description,
            "creation_date": self.creation_date

        }

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "project_name": "Sales Prediction",
                "project_description": "Predicting sales revenue"

            }
        }


class Analyze(BaseModel):
    forecast_days: int = Field(
        title="The number of days to be forcast into the future")
    project_name: str = Field(title="The project name")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "forecast_days": 365,
                "project_name": "project-1"

            }
        }


class Errors(BaseModel):
    loc: str
    msg: str
