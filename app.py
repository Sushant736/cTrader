from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables if running locally

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return {"message": "Backend live"}

@app.get("/equity/{account_id}")
def get_equity(account_id: str):
    client_id = os.getenv("CTRADER_CLIENT_ID")
    client_secret = os.getenv("CTRADER_CLIENT_SECRET")

    if not client_id or not client_secret:
        return {"error": "Missing client ID or secret in environment variables."}

    # 1. Get access token
    token_url = "https://live-api.ctrader.com/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = requests.post(token_url, data=payload, headers=headers)
    if token_response.status_code != 200:
        return {"error": "Failed to get access token", "details": token_response.text}

    access_token = token_response.json().get("access_token")

    # 2. Use token to fetch equity
    equity_url = f"https://api.ctrader.com/accounts/{account_id}/balance"
    headers = {"Authorization": f"Bearer {access_token}"}
    equity_response = requests.get(equity_url, headers=headers)

    if equity_response.status_code != 200:
        return {"error": "Failed to fetch account equity", "details": equity_response.text}

    return equity_response.json()
