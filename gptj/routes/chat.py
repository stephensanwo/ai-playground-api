import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, Cookie, Depends, FastAPI, Query, WebSocket, status, Request
from ..model.gptj import GPTJ
from ..middleware.cache import parse_data_to_cache, get_data_from_cache
from typing import Optional
import uuid
import aioredis

chat = APIRouter()

load_dotenv()
REDIS_AUTH = os.environ['REDIS_AUTH']

if os.environ["APP_ENV"] == "production":
    connection = f"redis://{REDIS_AUTH}@localhost:6379"

else:
    connection = "redis://localhost:6379"


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return session or token

# @route   POST /token
# @desc    Route generating chat token
# @access  Public


@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())
    client = request.client.host

    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    data = {"name": name, "token": token, "ip": client}

    redis = await aioredis.from_url(connection, db=6)
    await redis.set(token, str(data))

    return data


# @route   POST /refresh_token
# @desc    Route refreshing token
# @access  Public


@chat.post("/refresh_token")
async def refresh_token(token: str):

    redis = await aioredis.from_url(connection, db=6)
    await redis.delete(token)

    return None


# @route   Websocket /chat
# @desc    Route for gallium conversational bots
# @access  Public

@chat.websocket("/chat/{id}")
async def websocket_endpoint(websocket: WebSocket = WebSocket, id: str = str, token: Optional[str] = None, cookie_or_token: str = Depends(get_cookie_or_token), background_tasks: BackgroundTasks = BackgroundTasks()):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()

        await parse_data_to_cache(token=cookie_or_token, data={"Human": f"{data}"})

        history = await get_data_from_cache(token=cookie_or_token)

        context = f"""{history} Bot:"""

        print(context)

        # response = f"GPT-J-6b is currently offline, please try again later {id}"

        response = GPTJ.generate(context=context,
                                 token_max_length=128, temperature=1.0, top_probability=0.9)

        await parse_data_to_cache(token=cookie_or_token, data={"Bot": f"{response.strip()}"})

        await websocket.send_text(f"GPT-J BOT: {response}")
