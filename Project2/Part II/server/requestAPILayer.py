import requests
import urllib.parse

body_url = "https://github.com/Precioux/Cloud-Computing-Projects"
encoded_url = urllib.parse.quote(body_url, safe=':/')
print(f'after encoding: {encoded_url}')

url = "https://api.apilayer.com/short_url/hash"

payload = body_url.encode("utf-8")
headers= {
  "apikey": "8P71Zm1JorY60oeVYV7LXm9ID3VD2ICO"
}

response = requests.request("POST", url, headers=headers, data = payload)
data = response.json()

status_code = response.status_code
result = response.text
print(f'Status : {status_code}')
print(f'Result : {result} ')
print(f'Short : {data.get("short_url")}')