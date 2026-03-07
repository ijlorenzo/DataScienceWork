#!/usr/bin/env python3
"""
Quick script to generate a Google Ads refresh token.
Run this on your local machine (needs a browser).

Reads CLIENT_ID and CLIENT_SECRET from .env file or environment variables.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional, can use env vars directly

client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")

if not client_id or not client_secret:
    print("ERROR: Set GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET")
    print("Either in a .env file or as environment variables.")
    raise SystemExit(1)

CLIENT_CONFIG = {
    "installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

SCOPES = ["https://www.googleapis.com/auth/adwords"]

flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)
credentials = flow.run_local_server(port=0)

print("\n" + "=" * 60)
print("YOUR REFRESH TOKEN:")
print("=" * 60)
print(credentials.refresh_token)
print("=" * 60)
