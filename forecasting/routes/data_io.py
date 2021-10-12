from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi import FastAPI, HTTPException, status, Response, BackgroundTasks
from ..schema.model import Upload
from ..utils import validators
from ..utils.middleware import parse_data_cache
import os
from config import FORECAST_DATA_DIR
import aiofiles
import datetime

data_io = APIRouter()

# @route   POST /upload
# @desc    Create new forecasting analytics via data upload and metadata
# @access  Public


@data_io.post("/upload", status_code=201, response_model=Upload)
async def upload(file: UploadFile = File(...), email: str = Form(...), project_name: str = Form(...), project_description: str = Form(...), skip_nrows: int = Form(...), series_metric: str = Form(...), forecast_metric: str = Form(...), first_row_headers: bool = Form(...), request: Request = Request, background_tasks: BackgroundTasks = BackgroundTasks()):

    client = request.client.host

    # Validate user input
    errors, valid = validators.validateDataUpload(
        project_name, email, project_description, file)

    if not valid:
        raise HTTPException(status_code=400, detail=errors)

    # Validate that project name does not exist in cache
    errors, valid = await validators.validateProjectName(project_name)

    if not valid:
        raise HTTPException(status_code=400, detail=errors)

    async with aiofiles.open(os.path.join(FORECAST_DATA_DIR, file.filename), 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    # Validate the uploaded data
    errors, valid, data = validators.dataValidator(
        data_path=os.path.join(FORECAST_DATA_DIR, file.filename), skip_nrows=skip_nrows, series_metric=series_metric, forecast_metric=forecast_metric, first_row_headers=first_row_headers)

    if not valid:
        raise HTTPException(status_code=400, detail=errors)

    background_tasks.add_task(
        parse_data_cache, data, project_name, data_path=os.path.join(FORECAST_DATA_DIR, file.filename))

    return {"project_name": project_name,
            "project_description": project_description
            }
