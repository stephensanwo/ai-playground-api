from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..utils.middleware import get_data_from_cache
from ..algorithms.facebook_prophet import prophet_algorithm
from ..schema.model import Analyze

analytics = APIRouter()


# @route   POST /prophet-model
# @desc    Run base prophet analytics model
# @access  Public

@analytics.post("/prophet_model", status_code=201)
async def prophet_model(prophet_data: Analyze, background_tasks: BackgroundTasks):

    cache_df, errors, valid = await get_data_from_cache(prophet_data.project_name)

    if not valid:
        raise HTTPException(status_code=400, detail=errors)

    res = await prophet_algorithm(cache_df, forecast_days=prophet_data.forecast_days)

    return res
