from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Enable CORS (allow frontend apps to fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return {"message": "Backend live"}

@app.get("/equity/{account_id}")
def get_equity(account_id: str):
    try:
        # Read client credentials from environment
        client_id = os.getenv("CTRADER_CLIENT_ID")
        client_secret = os.getenv("CTRADER_CLIENT_SECRET")

        if not client_id or not client_secret:
            return {"error": "Missing CTRADER_CLIENT_ID or CTRADER_CLIENT_SECRET in Railway > Variables"}

        # STEP 1: Get access token
        token_url = "https://live-api.ctrader.com/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        token_response = requests.post(token_url, data=payload, headers=headers)
        print("Token Request Payload:", payload)
        print("Token Response Status:", token_response.status_code)
        print("Token Response Body:", token_response.text)

        if token_response.status_code != 200:
            return {"error": "Failed to get access token", "details": token_response.text}

        access_token = token_response.json().get("access_token")

        # STEP 2: Fetch account equity
        equity_url = f"https://api.ctrader.com/accounts/{account_id}/balance"
        headers = {"Authorization": f"Bearer {access_token}"}
        equity_response = requests.get(equity_url, headers=headers)

        print("Equity Request URL:", equity_url)
        print("Equity Response Status:", equity_response.status_code)
        print("Equity Response Body:", equity_response.text)

        if equity_response.status_code != 200:
            return {"error": "Failed to fetch account equity", "details": equity_response.text}

        return equity_response.json()

    except Exception as e:
        print("Exception occurred:", str(e))
        return {"error": "Internal error", "details": str(e)}
