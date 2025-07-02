from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
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
    redirect_uri = "https://ctrader-backend-production.up.railway.app/authorize"

    # Exchange the code for access & refresh tokens
    token_url = "https://connect.spotware.com/open-api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        return {
            "error": "Failed to get access token",
            "status": response.status_code,
            "details": response.text,
        }

    tokens = response.json()
    return {"message": "Authorization successful", "tokens": tokens}

# OPTIONAL: Placeholder for equity endpoint (can be used after token)
@app.get("/equity/{account_id}")
def get_equity(account_id: str):
    return {"message": f"Placeholder for equity of account {account_id}"}
