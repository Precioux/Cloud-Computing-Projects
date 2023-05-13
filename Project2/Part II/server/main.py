import redis
from fastapi import FastAPI
import json
import requests
import uvicorn
import time
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Access the config values
port = config["port"]
cache_expiry = config["cache_expiry"]
api_endpoint = config["api_endpoint"]
api_key = config["api_key"]
hostname = config['hostname']
redis_container_name = config['redis-server']
app = FastAPI()

# Connect to the Redis container
redis_client = redis.Redis(host=f"{redis_container_name}", port=port)

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
SHORT_URL_CACHE_EXPIRATION = cache_expiry

# Define API KEY
API_KEY = api_key


def toJSON(long_url, short_url, status):
    response = {
        "longUrl": long_url,
        "shortUrl": short_url,
        "isCached": status,
        "hostname": hostname
    }

    return json.dumps(response)


@app.get('/test')
async def test():
    return 'hey'


@app.get("/shorten_url/")
async def shorten_url(long_url: str):
    print(f'long URL : {long_url}')
    # Check if the short URL is already cached in Redis
    short_url = redis_client.get(long_url)
    if short_url:
        print(f'Was in Redis...')
        return toJSON(long_url, short_url.decode(), True)

    # If the short URL is not cached, call the Short URL API to get the short URL
    api_url = api_endpoint
    payload = long_url.encode("utf-8")
    headers = {"apikey": API_KEY}
    response = requests.request("POST", api_url, headers=headers, data=payload)
    status_code = response.status_code
    result = response.text
    print(f'Status : {status_code}')
    print(f'Result : {result} ')
    if response.status_code == 200:
        data = response.json()
        print(f'Shorten url : {data.get("short_url")}')
        # Cache the short URL in Redis with a expiration time of SHORT_URL_CACHE_EXPIRATION minutes
        redis_client.setex(long_url, SHORT_URL_CACHE_EXPIRATION * 60, data.get("short_url"))
        return toJSON(long_url, data.get("short_url"), False)
    else:
        return {"error": "Failed to shorten URL"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
