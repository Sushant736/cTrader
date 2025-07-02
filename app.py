from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Allow all origins (adjust later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend live ✅"}

@app.get("/authorize")
def authorize(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing authorization code"}

    client_id = os.getenv("CTRADER_CLIENT_ID")
    client_secret = os.getenv("CTRADER_CLIENT_SECRET")
    redirect_uri = "https://ctrader-backend-production.up.railway.app/authorize"

    token_url = "https://connect.spotware.com/apps/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        if response.status_code != 200:
            return {"error": "Failed to get token", "details": response.text}
        return response.json()
    except Exception as e:
        return {"error": "Token exchange failed", "details": str(e)}
