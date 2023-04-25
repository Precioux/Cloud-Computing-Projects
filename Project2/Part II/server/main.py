import redis
from fastapi import FastAPI
import json
import requests
import uvicorn
import time
app = FastAPI()


# Get the Redis container name
redis_container_name = "redis-cache"

# Connect to the Redis container
redis_client = redis.Redis(host=f"{redis_container_name}", port=6379)


# Wait for the Redis container to be ready
while True:
    try:
        if redis_client.ping():
            print("Redis container is active!")
            break
    except redis.exceptions.ConnectionError:
        print("Redis container is not yet ready. Waiting...")
        time.sleep(1)

# Define the expiration time for the short URLs cache in minutes
SHORT_URL_CACHE_EXPIRATION = 5

# Define API KEY
API_KEY = "8P71Zm1JorY60oeVYV7LXm9ID3VD2ICO"


def toJSON(long_url, short_url, status):
    response = {
        "longUrl": long_url,
        "shortUrl": short_url,
        "isCached": status,
        "hostname": "Nyx"
    }

    return json.dumps(response)


@app.get('/test')
async def test():
    return 'hey'


#curl http://localhost:8000/shorten_url/?long_url=https://aut.ac.ir/
@app.get("/shorten_url/")
async def shorten_url(long_url: str):
    print(f'long URL : {long_url}')
    # Check if the short URL is already cached in Redis
    short_url = redis_client.get(long_url)
    if short_url:
        return toJSON(long_url, short_url.decode(), True)

    # If the short URL is not cached, call the Short URL API to get the short URL
    api_url = f"https://api.apilayer.com/api/shorten?url={long_url}&apikey={API_KEY}"
    response = requests.get(api_url)
    if response.status_code == 200:
        short_url = response.json().get("result")
        # Cache the short URL in Redis with a expiration time of SHORT_URL_CACHE_EXPIRATION minutes
        redis_client.setex(
            long_url, SHORT_URL_CACHE_EXPIRATION * 60, short_url)
        return toJSON(long_url, short_url, False)
    else:
        return {"error": "Failed to shorten URL"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
