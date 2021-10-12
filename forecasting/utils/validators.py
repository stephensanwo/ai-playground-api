import re
import pandas as pd
import os
import asyncio
import aioredis

supported_files = [
    'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']


def validateDataUpload(project_name, email, project_description, file):
    errors = []

    # Validate String entries
    if project_name.strip() == "":
        errors.append(
            {"loc": "project_name", "msg": "Project name cannot be empty"})

    if project_description.strip() == "":
        errors.append({"loc": "project_description", "msg": "Project description cannot be empty"
                       })

    if len(project_name.strip()) > 50:
        errors.append(
            {"loc": "project_name", "msg": "Project name must be less than 50 characters"})

    if len(project_description.strip()) > 100:
        errors.append({
            "loc": "project_description",  "msg": "Project description must be less than 100 characters"})

     # Validate Email
    if email.strip() == "":
        errors.append({
            "loc": "email",  "msg": "Email is required"})

    else:
        regex = '^[a-z0-9]+(?:[._][a-z0-9]+)*@(?:\w+\.)+\w{2,3}$'
        if re.search(regex, email):
            pass
        else:
            errors.append({
                "loc": "project_description",  "msg": "Email must be valid"})

    # Validate File
    if file.content_type == "":
        errors.append({
            "loc": "file",  "msg": "File is required"})

    if file.content_type != "" and file.content_type not in supported_files:
        errors.append({
            "loc": "file",  "msg": "Unsuported file type"})

    valid = len(errors) < 1

    return errors, valid


async def validateProjectName(project_name):
    errors = []

    redis = await aioredis.from_url("redis://localhost:6379",  db=1)
    is_exists = await redis.exists(project_name)

    print(is_exists)

    if is_exists > 0:
        errors.append(
            {"loc": "project_name", "msg": "project name already exists, use a unique project name"})

    valid = len(errors) < 1

    return errors, valid


def dataValidator(*args, **kwargs):
    data_path = kwargs['data_path']
    skip_nrows = kwargs['skip_nrows']
    forecast_metric = kwargs['forecast_metric']
    series_metric = kwargs['series_metric']
    first_row_headers = kwargs['first_row_headers']
    errors = []

    file_name = data_path.split("/")[-1]
    file_extension = file_name.split(".")[1]

    # Input Validators
    if type(first_row_headers) != bool:
        errors.append(
            {"loc": "first_row_headers", "msg": "first_row_headers can either be true or false"})

    if skip_nrows < 0:
        errors.append(
            {"loc": "skip_nrows", "msg": "Enter a valid number of rows to skip"})

    # a. Import CSV

    if file_extension == "csv":
        data = pd.read_csv(data_path, skiprows=skip_nrows)

    # b. Import XLSX
    elif file_extension == "xlsx":
        data = pd.read_excel(data_path,  skiprows=skip_nrows)

    else:
        errors.append(
            {"loc": "file", "msg": "Upload a supported file type, .xlsx or .csv"})
        os.remove(data_path)

    # Validate metadata with data headers
    if series_metric not in list(data.columns):
        errors.append(
            {"loc": "series_metric", "msg": "series metric not found in uploded data"})
        try:
            os.remove(data_path)
        except:
            pass

    if forecast_metric not in list(data.columns):
        errors.append(
            {"loc": "forecast_metric", "msg": "forecast metric not found in uploded data"})
        try:
            os.remove(data_path)
        except:
            pass

    valid = len(errors) < 1

    return errors, valid, data
