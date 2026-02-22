import requests
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


# ✅ Read ONLY from env
backend_url = os.getenv("backend_url")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url")
print("BACKEND URL =", backend_url)
print("SENTIMENT URL =", sentiment_analyzer_url)

# ❌ Fail fast if env is missing
if not backend_url or not sentiment_analyzer_url:
    raise EnvironmentError(
        "backend_url or sentiment_analyzer_url missing in .env"
    )

# ✅ Normalize URLs (removes trailing slash issues)
backend_url = backend_url.rstrip("/")
sentiment_analyzer_url = sentiment_analyzer_url.rstrip("/")


# ---------------- GET REQUEST ----------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        params = "?" + "&".join(f"{k}={v}" for k, v in kwargs.items())

    request_url = f"{backend_url}{endpoint}{params}"
    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# ---------------- SENTIMENT ANALYSIS ----------------
def analyze_review_sentiments(text):
    encoded_text = urllib.parse.quote(text)
    request_url = f"{sentiment_analyzer_url}/analyze/{encoded_text}"
    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# ---------------- POST REVIEW ----------------
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url}")

    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None