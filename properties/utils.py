from django.core.cache import cache
from .models import Property
import logging


def get_all_properties():
    # Try to get the queryset from Redis
    properties = cache.get('all_properties')
    if properties is None:
        # If not in cache, fetch from DB
        properties = list(Property.objects.all())
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and calculates hit ratio.
    Returns a dictionary with hits, misses, and hit_ratio.
    """
    # Get the raw Redis client from django-redis
    redis_client = cache.client.get_client()

    # Fetch INFO stats
    info = redis_client.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    # Calculate hit ratio
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0


    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    }

    # Log metrics
    try:
        info = redis_client.info()
    except Exception as e:
        logger.error(f"Failed to retrieve Redis metrics: {e}")
    return {"hits": 0, "misses": 0, "hit_ratio": 0.0}
