# translator/translator.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def translate(text):
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"

    querystring = {
        "q": text,
        "langpair": "es|en",         # Translating from Spanish to English
        "mt": "1",
        "onlyprivate": "0",
        "de": "a@b.c"                # Required dummy email for API identification
    }

    headers = {
        "x-rapidapi-host": "translated-mymemory---translation-memory.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"[ERROR] {response.status_code} - {response.text}")
        response.raise_for_status()

    data = response.json()
    return data.get("responseData", {}).get("translatedText", "")
