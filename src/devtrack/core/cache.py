from devtrack.core.redis_client import redis_client
def build_cache_key(search,limit,offset):
    return f"projects:search={search}:limit={limit}:offset={offset}"

def invalidate_projects_cache():
    keys = redis_client.keys("projects:*")
    if keys:
        redis_client.delete(*keys)
