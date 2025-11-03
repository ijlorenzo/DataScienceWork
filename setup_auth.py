#!/usr/bin/env python3
"""
Helper script to generate Google Ads API refresh token
Run this script to authenticate and get your refresh token
"""

import sys

def generate_refresh_token():
    """Generate OAuth2 refresh token for Google Ads API"""

    print("=" * 60)
    print("Google Ads API Authentication Setup")
    print("=" * 60)
    print()

    print("This script will help you generate a refresh token for Google Ads API.")
    print()

    # Get credentials from user
    print("Please enter your OAuth2 credentials:")
    print("(You can find these in Google Cloud Console)")
    print()

    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    if not client_id or not client_secret:
        print("\nError: Client ID and Client Secret are required!")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Generating refresh token...")
    print("=" * 60)
    print()

    try:
        from google.ads.googleads.oauth2 import get_refresh_token

        # This will open a browser for authentication
        refresh_token = get_refresh_token(
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/adwords"]
        )

        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print()
        print("Your refresh token is:")
        print(refresh_token)
        print()
        print("Add this to your .env file as:")
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}")
        print()
        print("=" * 60)

        # Optionally save to .env file
        save = input("\nWould you like to save this to .env file? (y/n): ").strip().lower()
        if save == 'y':
            from dotenv import load_dotenv, set_key
            import os

            env_path = os.path.join(os.path.dirname(__file__), '.env')

            # Create .env from .env.example if it doesn't exist
            if not os.path.exists(env_path):
                example_path = os.path.join(os.path.dirname(__file__), '.env.example')
                if os.path.exists(example_path):
                    with open(example_path, 'r') as f:
                        with open(env_path, 'w') as out:
                            out.write(f.read())

            # Update values
            set_key(env_path, "GOOGLE_ADS_CLIENT_ID", client_id)
            set_key(env_path, "GOOGLE_ADS_CLIENT_SECRET", client_secret)
            set_key(env_path, "GOOGLE_ADS_REFRESH_TOKEN", refresh_token)

            print(f"\nCredentials saved to {env_path}")
            print("Don't forget to also add:")
            print("  - GOOGLE_ADS_DEVELOPER_TOKEN")
            print("  - GOOGLE_ADS_LOGIN_CUSTOMER_ID")
            print("  - GOOGLE_ADS_CUSTOMER_ID")

    except ImportError:
        print("\nError: google-ads library not installed.")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\nError generating refresh token: {str(e)}")
        print("\nAlternatively, you can use the Google Ads API tool:")
        print(f"python -m google.ads.googleads.oauth2.generate_user_credentials \\")
        print(f"  --client_id {client_id} \\")
        print(f"  --client_secret {client_secret}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        generate_refresh_token()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
