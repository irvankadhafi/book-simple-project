import redis
from app.config.config import config


redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

def get_redis():
    return redis_client
