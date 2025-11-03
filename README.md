# Google Ads MCP Server

A Model Context Protocol (MCP) server for querying Google Ads data using natural language. This server enables you to retrieve campaign performance, keyword data, search terms, and other Google Ads metrics through simple natural language queries or GAQL (Google Ads Query Language).

## Features

- **Natural Language Queries**: Ask questions in plain English about your Google Ads performance
- **GAQL Support**: Execute custom Google Ads Query Language queries
- **Common Query Templates**: Pre-built queries for common use cases
- **MCP Integration**: Works with any MCP-compatible client (Claude Desktop, etc.)

## Prerequisites

1. **Google Ads Account** with API access
2. **Google Ads Developer Token** ([Get one here](https://developers.google.com/google-ads/api/docs/first-call/dev-token))
3. **OAuth2 Credentials** (Client ID, Client Secret, Refresh Token)
4. **Python 3.8+**

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Google Ads API Access

1. **Get a Developer Token**:
   - Go to [Google Ads API Center](https://ads.google.com/aw/apicenter)
   - Apply for a developer token
   - Note: You can use a test account developer token for testing

2. **Set up OAuth2 Credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Ads API
   - Create OAuth2 credentials (Desktop Application)
   - Download the credentials

3. **Generate a Refresh Token**:
   ```bash
   # Use the Google Ads API authentication helper
   python -m google.ads.googleads.oauth2.generate_user_credentials \
     --client_id YOUR_CLIENT_ID \
     --client_secret YOUR_CLIENT_SECRET
   ```

   This will open a browser window for you to authorize access and will output a refresh token.

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```bash
   GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token_here
   GOOGLE_ADS_CLIENT_ID=your_client_id_here
   GOOGLE_ADS_CLIENT_SECRET=your_client_secret_here
   GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token_here
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
   GOOGLE_ADS_CUSTOMER_ID=1234567890
   ```

   **Note**:
   - `LOGIN_CUSTOMER_ID` is your manager account ID (if you have one), otherwise use your customer ID
   - `CUSTOMER_ID` is the account you want to query
   - Remove any hyphens from the customer IDs

### Step 4: Test the Server

Run the server in test mode:

```bash
python google_ads_mcp_server.py
```

## MCP Client Configuration

### Claude Desktop Configuration

Add this to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["/home/user/DataScienceWork/google_ads_mcp_server.py"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your_token",
        "GOOGLE_ADS_CLIENT_ID": "your_client_id",
        "GOOGLE_ADS_CLIENT_SECRET": "your_client_secret",
        "GOOGLE_ADS_REFRESH_TOKEN": "your_refresh_token",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "1234567890",
        "GOOGLE_ADS_CUSTOMER_ID": "1234567890"
      }
    }
  }
}
```

**Or use the .env file approach**:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["/home/user/DataScienceWork/google_ads_mcp_server.py"],
      "cwd": "/home/user/DataScienceWork"
    }
  }
}
```

After updating the config, restart Claude Desktop.

## Usage Examples

### Natural Language Queries

Once the MCP server is connected, you can ask questions like:

- "Show me my campaign performance"
- "What are my top performing campaigns?"
- "Give me keyword performance data"
- "Show me search terms"
- "What's my account overview?"

### Available Tools

#### 1. `query_google_ads`

Query Google Ads data using natural language or GAQL.

**Supported natural language patterns**:
- `campaign performance` - Get metrics for all campaigns
- `ad group performance` - Get metrics for all ad groups
- `keyword performance` - Get keyword metrics
- `search terms` - Get search term data
- `account overview` - Get overall account metrics
- `top performing campaigns` - Get best campaigns by conversions

**Custom GAQL queries**:
```
SELECT campaign.name, metrics.impressions, metrics.clicks
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
```

#### 2. `get_account_info`

Get basic information about your Google Ads account.

#### 3. `list_campaigns`

List all campaigns with optional status filtering (ENABLED, PAUSED, REMOVED, ALL).

## Query Examples

### Example 1: Campaign Performance
```
Show me campaign performance for the last 30 days
```

Returns: Campaign names, impressions, clicks, cost, conversions, CTR, and average CPC.

### Example 2: Top Performers
```
What are my top 10 performing campaigns?
```

Returns: Top 10 campaigns sorted by conversions.

### Example 3: Custom GAQL
```
SELECT ad_group.name, metrics.impressions, metrics.clicks
FROM ad_group
WHERE campaign.id = 12345
AND segments.date DURING LAST_7_DAYS
```

Returns: Custom query results based on your GAQL.

## Metrics Available

Common metrics you can query:
- `metrics.impressions` - Number of impressions
- `metrics.clicks` - Number of clicks
- `metrics.cost_micros` - Cost in micros (divide by 1,000,000 for actual cost)
- `metrics.conversions` - Number of conversions
- `metrics.ctr` - Click-through rate
- `metrics.average_cpc` - Average cost per click
- `metrics.conversions_value` - Total conversion value

[Full list of metrics](https://developers.google.com/google-ads/api/fields/v16/metrics)

## Resources

Available resources:
- `googleads://account/info` - Current account information

## Troubleshooting

### Authentication Errors

If you get authentication errors:
1. Verify your developer token is correct
2. Check that your OAuth2 credentials are valid
3. Regenerate your refresh token if needed
4. Ensure customer IDs don't have hyphens

### Query Errors

If queries fail:
1. Check the [GAQL documentation](https://developers.google.com/google-ads/api/docs/query/overview)
2. Verify date ranges are valid
3. Ensure you have data in your account
4. Check API quotas and limits

### Connection Issues

If the MCP server won't connect:
1. Verify the path in your MCP client config
2. Check that Python dependencies are installed
3. Ensure `.env` file is in the correct location
4. Check logs for specific error messages

## Extending the Server

### Adding Custom Query Templates

Edit the `natural_language_to_gaql()` function in `google_ads_mcp_server.py` to add new natural language patterns:

```python
patterns = {
    "your custom pattern": """
        SELECT ...
        FROM ...
        WHERE ...
    """
}
```

### Adding New Tools

Add new tools in the `@app.list_tools()` decorator and handle them in `@app.call_tool()`.

## Resources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [GAQL Reference](https://developers.google.com/google-ads/api/docs/query/overview)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Available Fields and Metrics](https://developers.google.com/google-ads/api/fields/v16/overview)

## License

MIT License - Feel free to modify and use as needed.

## Support

For issues or questions:
1. Check the Google Ads API documentation
2. Verify your credentials and permissions
3. Review the troubleshooting section above
4. Check MCP client logs for detailed error messages
