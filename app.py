from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend live and ready"}

@app.get("/authorize")
def authorize(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing authorization code"}

    client_id = os.getenv("CTRADER_CLIENT_ID")
    client_secret = os.getenv("CTRADER_CLIENT_SECRET")
    redirect_uri = "https://ctrader-production.up.railway.app/authorize"

    token_url = "https://connect.spotware.com/open-api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        if response.status_code != 200:
            return {
                "error": "Failed to get access token",
                "status": response.status_code,
                "text": response.text
            }

        tokens = response.json()
        return {"message": "Authorization successful", "tokens": tokens}

    except Exception as e:
        return {"error": "Internal exception", "details": str(e)}
