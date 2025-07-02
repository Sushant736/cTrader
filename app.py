from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
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
        return {"error": "Missing authorization code in query parameter"}

    # ✅ Your credentials
    client_id = "11434_ZZJnszRiyYFBn7qoPMdizSF1bKtOgSOnrkN8ujxKhmQoktRhua"
    client_secret = "rbH4Qrax259nAtf1EdHmKibpQL1Yp0bkdCPcq4fgTgGgAYannf"
    redirect_uri = "https://ctrader-production.up.railway.app/authorize"

    token_url = "https://connect.spotware.com/apps/token"
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

        return {
            "message": "Authorization successful",
            "tokens": response.json()
        }

    except Exception as e:
        return {"error": "Internal error", "details": str(e)}

# Optional placeholder to test route setup
@app.get("/equity/{account_id}")
def get_equity(account_id: str):
    return {"message": f"Placeholder - Equity info for account {account_id} will be here"}
