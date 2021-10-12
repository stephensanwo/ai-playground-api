import pandas as pd
import os
from prophet import Prophet


async def prophet_algorithm(cache_df, forecast_days):

    m = Prophet()
    m.fit(cache_df)
    future = m.make_future_dataframe(periods=forecast_days)
    forecast = m.predict(future)

    return forecast.to_json(orient="records")
