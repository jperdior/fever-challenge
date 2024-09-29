"""Redis cache implementation."""
import os
import redis as redis_client

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

CACHE = redis_client.Redis(host=REDIS_HOST, port=REDIS_PORT)
