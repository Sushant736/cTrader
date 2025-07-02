from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, os

app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ping():
    return {"message": "Backend live"}

# ✅ 1. Exchange Authorization Code for Access Token
@app.get("/authorize")
def authorize(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code missing in URL"}

    token_url = "https://live-api.ctrader.com/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("CTRADER_CLIENT_ID"),
        "client_secret": os.getenv("CTRADER_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": "https://ctrader-backend-production.up.railway.app/authorize"  # ✅ must match registered URL
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to exchange code", "details": response.text}

    return response.json()  # ✅ Includes access_token, refresh_token

# ✅ 2. Get Accounts using Access Token
@app.get("/accounts")
def get_accounts(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.ctrader.com/accounts", headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch accounts", "details": response.text}

    return response.json()

# ✅ 3. Get Equity/Balance using Account ID
@app.get("/equity/{account_id}")
def get_equity(account_id: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.ctrader.com/accounts/{account_id}/balance"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch balance", "details": response.text}

    return response.json()
