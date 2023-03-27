import email

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
id = 11
email = 'sa.mahdipour@gmail.com'
inputs = ''
language = 'py'
enable = 0
url = "http://localhost:8000/submit_email/?id={}&email={}&inputs={}&language={}&enable={}".format(id, email, inputs, language, enable)
file_path = "C:/Users/Samin/Desktop/samin.py"

files = {'file': open(file_path, 'rb')}

encoder = MultipartEncoder(fields={
    'file': ('file', open(file_path, 'rb'), 'application/octet-stream')
})

headers = {
    'Content-Type': encoder.content_type,
}

response = requests.post(url, headers=headers, data=encoder.to_string())

if response.status_code == 422:
    print("Error: 422 Unprocessable Entity")
    print(response.text)
    # Print any relevant log entries from the server logs here
else:
    print(response.text)
