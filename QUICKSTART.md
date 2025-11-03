# Quick Start Guide

Get your Google Ads MCP server up and running in 5 steps!

## Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

## Step 2: Get Google Ads API Credentials (10-15 minutes)

### A. Get Developer Token

1. Go to https://ads.google.com/aw/apicenter
2. Click "Apply for access" to get a developer token
3. For testing, you can use a test account token immediately

### B. Set up OAuth2 Credentials

1. Go to https://console.cloud.google.com/
2. Create or select a project
3. Enable "Google Ads API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Choose "Desktop Application"
6. Download the credentials (or copy Client ID and Client Secret)

## Step 3: Generate Refresh Token (2 minutes)

Run the setup helper:

```bash
python setup_auth.py
```

This will:
- Prompt for your Client ID and Client Secret
- Open a browser for you to authorize
- Generate and save your refresh token to `.env`

**OR** use the Google Ads command:

```bash
python -m google.ads.googleads.oauth2.generate_user_credentials \
  --client_id YOUR_CLIENT_ID \
  --client_secret YOUR_CLIENT_SECRET
```

## Step 4: Complete .env Configuration (1 minute)

Edit `.env` and add your remaining credentials:

```bash
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
GOOGLE_ADS_CLIENT_ID=your_client_id
GOOGLE_ADS_CLIENT_SECRET=your_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890  # Your manager account or customer ID
GOOGLE_ADS_CUSTOMER_ID=1234567890        # The account you want to query
```

**Important**: Remove any hyphens from customer IDs!
- Wrong: `123-456-7890`
- Right: `1234567890`

## Step 5: Test the Connection (1 minute)

```bash
python test_connection.py
```

This will verify:
- Your credentials are valid
- You can connect to Google Ads API
- You can query data from your account

## Step 6: Connect to Claude Desktop (5 minutes)

### macOS

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

### Linux

Edit: `~/.config/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["/absolute/path/to/google_ads_mcp_server.py"],
      "cwd": "/absolute/path/to/DataScienceWork"
    }
  }
}
```

**Update the paths** to match your system!

Then **restart Claude Desktop**.

## Step 7: Start Querying! (now)

In Claude Desktop, try asking:

- "Show me my campaign performance"
- "What are my top performing campaigns?"
- "Give me keyword performance data"
- "What's my account overview?"

## Troubleshooting

### "Invalid client_customer_id"
- Remove hyphens from customer ID in `.env`
- Use format: `1234567890` not `123-456-7890`

### "Developer token is invalid"
- Check you copied the full token
- For testing, use test account token
- Production tokens need Google approval

### "Authentication failed"
- Regenerate your refresh token with `python setup_auth.py`
- Verify Client ID and Secret are correct
- Check that OAuth consent screen is configured

### "No data returned"
- Verify your account has active campaigns
- Check date ranges in queries (default is LAST_30_DAYS)
- Ensure you're querying the correct customer ID

### MCP Server Not Connecting
- Check the path in `claude_desktop_config.json` is absolute
- Ensure Python is in your system PATH
- Try running the server manually first: `python google_ads_mcp_server.py`
- Check Claude Desktop logs for error messages

## Need Help?

1. See full [README.md](README.md) for detailed documentation
2. Check [Google Ads API docs](https://developers.google.com/google-ads/api/docs/start)
3. Review [MCP documentation](https://modelcontextprotocol.io/)

## What's Next?

- Explore custom GAQL queries
- Add your own query templates
- Query specific campaigns or date ranges
- Export data for analysis

Enjoy querying your Google Ads data in natural language!
