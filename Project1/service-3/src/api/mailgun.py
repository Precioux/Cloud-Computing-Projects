import requests

DOMAIN = "sandbox7eaadbbead3e419fbb5da0c3c49b2b5e.mailgun.org"
API_KEY = "0b7b57a4d29ac9e1041a838a530fa5d9-d51642fa-0c4f5347"
TEXT = TEXT = f"""
        <h1>BOOO </h1>

        """
SUBJECT = "Cloud Computing Project 1 - Mail Service"
EMAIL_ADDRESS = "uni.mahdipour@gmail.com"


def send_simple_message(email, subject, text):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data={"from": f"<mailgun@{DOMAIN}>",
              "to": [email],
              "subject": subject,
              "html": text})


if __name__ == '__main__':
    response = send_simple_message(EMAIL_ADDRESS, SUBJECT, TEXT)
    print(response.json())