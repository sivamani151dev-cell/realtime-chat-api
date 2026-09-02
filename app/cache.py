import redis.asyncio as aioredis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def get_redis():
    return await aioredis.from_url(REDIS_URL, decode_responses=True)

async def publish_message(channel: str, message: dict):
    redis = await get_redis()
    await redis.publish(channel, json.dumps(message))
    await redis.close()

async def subscribe_to_channel(channel: str):
    redis = await get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    return pubsub, redis