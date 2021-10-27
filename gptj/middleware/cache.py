import asyncio
import aioredis
import json
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_AUTH = os.environ['REDIS_AUTH']

if os.environ["APP_ENV"] == "production":
    connection = f"redis://{REDIS_AUTH}@178.62.22.115:6379"

else:
    connection = "redis://localhost:6379"


async def parse_data_to_cache(token, data):

    redis = await aioredis.from_url(connection, db=5)

    token_exists = await redis.exists(token)

    if token_exists == 0:
        await redis.rpush(token, json.dumps(data))

    else:
        await redis.rpush(token, json.dumps(data))

    await redis.expire(token, 3600)

    return token_exists


def parse_to_str(x):

    output = "".join(str(list(json.loads(x).keys())
                         [0])) + ": " + str(list(json.loads(x).values())[0])

    return output


async def get_data_from_cache(token):

    redis = await aioredis.from_url(connection, db=5)

    token_exists = await redis.exists(token)

    if token_exists == 0:
        res = []
        pass

    else:
        res = await redis.lrange(token, start=0, end=-1)
        res = map(parse_to_str, res)

    res = " ".join(res)

    return res


if __name__ == "__main__":
    # res = asyncio.run(parse_data_to_cache(token="2323ferf",
    #                                       data={"Human": "Hello"}))

    res = asyncio.run(get_data_from_cache(token="token"))
