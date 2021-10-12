import asyncio
import aioredis
import os
import pandas as pd


async def parse_data_cache(data, project_name, data_path):

    data_json = data.to_json(orient='records')

    redis = await aioredis.from_url("redis://localhost:6379",  db=1)

    await redis.set(project_name, data_json)

    await redis.expire(project_name, 3600)

    try:
        await os.remove(data_path)
    except:
        pass

    return data_json


async def get_data_from_cache(project_name):
    errors = []
    redis = await aioredis.from_url("redis://localhost:6379",  db=1)

    data_json = await redis.get(project_name)

    try:
        cache_df = pd.read_json(data_json)
    except:
        # Validate Result
        errors.append({
            "loc": "file",  "msg": "Data cache time limit has expired, re-upload the data and try again"})

        cache_df = []

    valid = len(errors) < 1

    return cache_df, errors, valid


# async def parse_result_to_cache(data, project_name):

#     data_json = data.to_json(orient='records')

#     redis = await aioredis.from_url("redis://localhost:6379",  db=2)

#     await redis.set(project_name, data_json)

#     await redis.expire(project_name, 3600)

#     return data_json
