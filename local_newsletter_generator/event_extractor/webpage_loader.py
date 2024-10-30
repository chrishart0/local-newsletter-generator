from langchain_community.document_loaders import WebBaseLoader
from cachetools import TTLCache, cached
import pickle
import os

# Get the configured logger
from local_newsletter_generator.helpers.logger_helper import get_logger

logger = get_logger()

CACHE_DIR = ".cache"
CACHE_FILE = os.path.join(CACHE_DIR, "webpage_loader_persistent_cache.pkl")
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Ensure the cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Load cache from file if it exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = TTLCache(maxsize=100, ttl=CACHE_EXPIRY)


def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)


@cached(cache)
def load_webpage(url: str) -> str:
    # Check if the cache already has the document
    if url in cache:
        logger.info("Using cached document.")
        return cache[url]
    else:
        logger.info(f"Loading webpage from {url} and caching it.")

    # Load the webpage and cache the document
    loader = WebBaseLoader(url)
    document = loader.load()

    # Cache the document
    cache[url] = document

    # Save the cache to file
    save_cache()

    return document
