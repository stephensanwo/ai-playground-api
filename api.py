from fastapi import FastAPI
from forecasting.routes import data_io
import uvicorn
from forecasting.routes.data_io import data_io
from forecasting.routes.analytics import analytics
from gptj.routes.chat import chat
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()
api.include_router(data_io)
api.include_router(analytics)
api.include_router(chat)

origins = [
    "http://localhost:3019",
    "http://192.168.0.149:3019d"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/test")
async def root():
    return 'Success'


if __name__ == "__main__":
    uvicorn.run("api:api", host="0.0.0.0", port=8558, reload=True)
