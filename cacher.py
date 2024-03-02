import redis
import hashlib

# Configuration
elasticache_config_endpoint = "your-elasticache-cluster-endpoint"
redis_client = redis.StrictRedis(
    host=elasticache_config_endpoint, port=6379, db=0, decode_responses=True
)


def generate_cache_key(input_text):
    return hashlib.sha256(input_text.encode("utf-8")).hexdigest()


def get_response(input_text):
    cache_key = generate_cache_key(input_text)
    cached_response = redis_client.get(cache_key)
    if cached_response:
        return cached_response  # Return from cache
    else:
        # Process the request to generate response
        response = process_request(input_text)
        # Cache the response
        redis_client.setex(cache_key, 3600, response)  # Cache for 1 hour
        return response
