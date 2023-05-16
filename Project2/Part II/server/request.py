import json
import requests

url = "http://localhost:8000/shorten_url/"
long_url = "https://www.careerplanner.com/8CognitiveFunctions/Cognitive-Functions-Simply-Explained.cfm"
payload = {
    "long_url": long_url
}
headers = {
    "Accept": "application/json"
}

response = requests.get(url, params=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    res = json.dumps(data)
    print(f"Response: {res}")
else:
    print("Failed to shorten URL")
