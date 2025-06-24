import os
import requests
from dotenv import load_dotenv

load_dotenv()

def translate(text):
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {
        "to": "en",
        "api-version": "3.0",
        "from": "es",
        "profanityAction": "NoAction",
        "textType": "plain"
    }

    payload = [{"Text": text}]

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST")
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"[ERROR] {response.status_code} - {response.text}")
        response.raise_for_status()

    return response.json()[0]['translations'][0]['text']
