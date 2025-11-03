#!/usr/bin/env python3
"""
Test script to verify Google Ads API connection and credentials
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    print("=" * 70)
    print("Checking Environment Variables")
    print("=" * 70)

    required_vars = [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_CUSTOMER_ID"
    ]

    optional_vars = [
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID"
    ]

    all_present = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if len(value) > 10:
                masked = value[:4] + "*" * (len(value) - 8) + value[-4:]
            else:
                masked = "*" * len(value)
            print(f"✓ {var}: {masked}")
        else:
            print(f"✗ {var}: NOT SET")
            all_present = False

    for var in optional_vars:
        value = os.getenv(var)
        if value:
            if len(value) > 10:
                masked = value[:4] + "*" * (len(value) - 8) + value[-4:]
            else:
                masked = "*" * len(value)
            print(f"○ {var}: {masked} (optional)")
        else:
            print(f"○ {var}: NOT SET (optional)")

    print()

    if not all_present:
        print("❌ ERROR: Some required environment variables are missing!")
        print("Please check your .env file.")
        return False

    # Check customer ID format
    customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")
    if "-" in customer_id:
        print("⚠️  WARNING: GOOGLE_ADS_CUSTOMER_ID contains hyphens")
        print(f"   Current: {customer_id}")
        print(f"   Should be: {customer_id.replace('-', '')}")
        print("   Customer IDs should not contain hyphens!")
        print()

    return all_present


def test_import():
    """Test if required packages are installed"""
    print("=" * 70)
    print("Checking Python Dependencies")
    print("=" * 70)

    packages = {
        "mcp": "MCP SDK",
        "google.ads.googleads": "Google Ads API",
        "dotenv": "Python Dotenv"
    }

    all_installed = True

    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name}: Installed")
        except ImportError:
            print(f"✗ {name}: NOT INSTALLED")
            all_installed = False

    print()

    if not all_installed:
        print("❌ ERROR: Some required packages are missing!")
        print("Run: pip install -r requirements.txt")
        return False

    return True


def test_connection():
    """Test connection to Google Ads API"""
    print("=" * 70)
    print("Testing Google Ads API Connection")
    print("=" * 70)

    try:
        from google.ads.googleads.client import GoogleAdsClient
        from google.ads.googleads.errors import GoogleAdsException

        # Initialize client
        credentials = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True
        }

        print("Initializing Google Ads client...")
        client = GoogleAdsClient.load_from_dict(credentials)
        print("✓ Client initialized successfully")
        print()

        # Get customer ID
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")

        # Test basic query
        print(f"Testing query for customer ID: {customer_id}")
        query = """
            SELECT
                customer.id,
                customer.descriptive_name,
                customer.currency_code,
                customer.time_zone
            FROM customer
            LIMIT 1
        """

        ga_service = client.get_service("GoogleAdsService")
        stream = ga_service.search_stream(customer_id=customer_id, query=query)

        print("Executing test query...")

        for batch in stream:
            for row in batch.results:
                print()
                print("✓ Successfully connected to Google Ads API!")
                print()
                print(f"Account Details:")
                print(f"  ID: {row.customer.id}")
                print(f"  Name: {row.customer.descriptive_name}")
                print(f"  Currency: {row.customer.currency_code}")
                print(f"  Timezone: {row.customer.time_zone}")
                print()
                return True

        return True

    except GoogleAdsException as ex:
        print()
        print(f"❌ Google Ads API Error: {ex.error.message}")
        print()
        print("Error details:")
        for error in ex.failure.errors:
            print(f"  - {error.message}")
            if error.error_code:
                print(f"    Code: {error.error_code}")
        print()
        print("Common issues:")
        print("  1. Developer token is invalid or not approved")
        print("  2. OAuth credentials are incorrect")
        print("  3. Customer ID is incorrect or has no access")
        print("  4. Refresh token has expired")
        print()
        return False

    except Exception as e:
        print()
        print(f"❌ Unexpected error: {str(e)}")
        print()
        return False


def test_sample_queries():
    """Test some sample queries"""
    print("=" * 70)
    print("Testing Sample Queries")
    print("=" * 70)

    try:
        from google.ads.googleads.client import GoogleAdsClient

        credentials = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
            "use_proto_plus": True
        }

        client = GoogleAdsClient.load_from_dict(credentials)
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")

        # Test campaign query
        query = """
            SELECT
                campaign.id,
                campaign.name,
                campaign.status
            FROM campaign
            LIMIT 5
        """

        print("Fetching campaigns...")
        ga_service = client.get_service("GoogleAdsService")
        stream = ga_service.search_stream(customer_id=customer_id, query=query)

        count = 0
        for batch in stream:
            for row in batch.results:
                count += 1
                print(f"  Campaign: {row.campaign.name} (Status: {row.campaign.status.name})")

        if count > 0:
            print(f"\n✓ Found {count} campaign(s)")
        else:
            print("\n⚠️  No campaigns found (this is OK if your account is new)")

        print()
        return True

    except Exception as e:
        print(f"❌ Error testing queries: {str(e)}")
        print()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" Google Ads MCP Server - Connection Test")
    print("=" * 70)
    print()

    # Check environment
    if not check_environment():
        sys.exit(1)

    # Check dependencies
    if not test_import():
        sys.exit(1)

    # Test connection
    if not test_connection():
        sys.exit(1)

    # Test sample queries
    test_sample_queries()

    # Success message
    print("=" * 70)
    print(" 🎉 All tests passed! Your setup is ready.")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Configure your MCP client (e.g., Claude Desktop)")
    print("2. Start querying your Google Ads data!")
    print()
    print("Try questions like:")
    print("  - 'Show me my campaign performance'")
    print("  - 'What are my top performing campaigns?'")
    print("  - 'Give me keyword performance data'")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
